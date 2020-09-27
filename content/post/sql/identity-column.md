---
title: "SQL Server: Make a column an identity"
date: 2017-10-13
category:
- database
tags:
- MSSQL
---

In SQL Server, columns can be defined as an identity column. With an identity
column, each newly inserted row will get a new unique value in the identity
column. This is useful for auto-incrementing a primary key column.

There are cases when a primary key column is not set up as an identity. This
requires each INSERT statement to explicitly set the new ID value. Changing an
existing column to be an identity column turns out to be nontrivial. The
sections below explain the steps. See the last code block for a generic SQL
template to use.

_**Note**_: changing a primary key column involves dropping the column and
renaming a new identity column. Therefore this recipe would not apply if there
are any foreign key references to the primary key column.

# Steps

The steps below explain how an example @Customer@ table can be updated. It has a
primary key called Cust_ID that is initially not an identity field. The steps
below show what was needed to change this column to be an identity column.

### Create a new identity column

An existing column cannot simply be altered to be an identity column. We need to
create a new identity column first. This needs to be done in a separate IF
block, followed by a GO:

    :::sql
    IF (SELECT columnproperty(object_id('Customer'),'Cust_ID','IsIdentity')) = 0 
        ALTER TABLE Customer ADD Cust_New_ID int IDENTITY
    GO

The remaining steps are all within an IF block, like so:

    :::sql
    IF (SELECT columnproperty(object_id('Customer'),'Cust_ID','IsIdentity')) = 0 
    BEGIN
        -- content of remaining steps (below) go here
    END

Yes, we already have a similar IF block above. It is necessary to commit this
new column first, before applying the next steps.

### Duplicate the existing rows

Next, we need to populate the newly created identity column (Cust_New_ID in this
example) to contain the existing primary key values of the Cust_ID column.  We
do so by simply duplicating the existing rows.

    :::sql
    -- Duplicate the rows, and set the old Cust_ID IDs into the new
    Cust_New_ID column:
    set identity_insert Customer on
    DECLARE @intMAXID int, @sql NVARCHAR(512)
    SELECT @intMaxID = max(Cust_ID) from Customer
    INSERT INTO Customer (
        Cust_New_ID,
        Cust_ID,
        Cust_Name,
        Cust_Currency,
        Cust_Email) 
    SELECT Cust_ID,
        @intMAXID + row_number() over (order by Cust_ID),
        Cust_Name,
        Cust_Currency,
        Cust_Email
    FROM Customer
    set identity_insert Customer off

_**Note**_: 

* Normally the identity column manages its value automatically. In this case we
  need to populate it with the original primary key values. The line with "set
  identity_insert Customer on" allows us to insert values manually.
* Before inserting the duplicate rows, remember the maximum primary key value in
  variable @intMAXID. This allows us to delete the old rows in the next step

### Delete the original rows

Delete the original rows, so we don't have duplicates:

    :::sql
    delete from Customer where Cust_ID <= @intMAXID

### Drop the original primary key column

Now that we have a new identity column with the values of the old primary key
column, drop the primary key column.
Note: We first need to remove the primary key contraint from the column, before
we can remove the column:

    :::sql
    SELECT @sql = 'ALTER TABLE Customer'
        + ' DROP CONSTRAINT ' + name + ';'
        FROM sys.key_constraints
        WHERE type = 'PK'
        AND parent_object_id = OBJECT_ID('Customer');
    EXEC sp_executeSQL @sql;
    ALTER TABLE Customer DROP COLUMN Cust_ID

### Update the newly created identity column and make it the primary key

Finally, rename the newly created identity column to the name of the original
primary key column.
Then make it the new primary key

    :::sql
    exec sp_rename 'Customer.Cust_New_ID', 'Cust_ID', 'column'
    ALTER TABLE Customer ALTER COLUMN Cust_ID INT NOT NULL
    ALTER TABLE Customer ADD CONSTRAINT [PK_Customer] PRIMARY KEY(Cust_ID);

# Generic Template Script

Below is a complete code block that can be used as a template.

Substitute the following:

* MY_TABLE with your actual table name
* MY_KEY_COLUM with your table's primary key column name
* MY_OTHER_COLUM with a list of all the remaining columns of your table
* MY_PK_NAME with the name of the table's primary key constraint

---

    :::sql
    IF (SELECT columnproperty(object_id('MY_TABLE'),'MY_KEY_COLUMN','IsIdentity')) = 0 
        ALTER TABLE MY_TABLE ADD MY_NEW_IDENTITY_COLUMN int IDENTITY
    GO
    
    IF (SELECT columnproperty(object_id('MY_TABLE'),'MY_KEY_COLUMN','IsIdentity')) = 0 
    BEGIN
        -- Duplicate the rows, and set the old MY_KEY_COLUMN IDs into the new MY_NEW_IDENTITY_COLUMN column:
        set identity_insert MY_TABLE on
        DECLARE @intMAXID int, @sql NVARCHAR(512)
        SELECT @intMaxID = max(MY_KEY_COLUMN) from MY_TABLE

        SELECT @sql = 'INSERT INTO MY_TABLE (
            MY_NEW_IDENTITY_COLUMN,
            MY_OTHER_COLUMN) 
        SELECT MY_KEY_COLUMN, ' + CAST(@intMAXID AS VARCHAR(10)) + ' + row_number() over (order by MY_KEY_COLUMN),
            MY_OTHER_COLUMN,
        FROM MY_TABLE'

        EXEC sp_executeSQL @sql;
        set identity_insert MY_TABLE off
     
        -- Delete the original rows, so we don't have duplicates:
        delete from MY_TABLE where MY_KEY_COLUMN <= @intMAXID
    
        -- Make MY_NEW_IDENTITY_COLUMN the new MY_KEY_COLUMN column:
        -- First need to drop the PK constraint and then drop MY_KEY_COLUMN:
        SELECT @sql = 'ALTER TABLE MY_TABLE'
            + ' DROP CONSTRAINT ' + name + ';'
            FROM sys.key_constraints
            WHERE type = 'PK'
            AND parent_object_id = OBJECT_ID('MY_TABLE');
        EXEC sp_executeSQL @sql;
        ALTER TABLE MY_TABLE DROP COLUMN MY_KEY_COLUMN
        
        -- Then rename column so we have a new MY_KEY_COLUMN with PK constraint:
        exec sp_rename 'MY_TABLE.MY_NEW_IDENTITY_COLUMN', 'MY_KEY_COLUMN', 'column'
        ALTER TABLE MY_TABLE ALTER COLUMN MY_KEY_COLUMN INT NOT NULL
        ALTER TABLE MY_TABLE ADD CONSTRAINT [MY_PK_NAME] PRIMARY KEY(MY_KEY_COLUMN);
    END

