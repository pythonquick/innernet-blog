Title: Using Raspberry Pi to calculate pi
Date: 2018-03-14
Category: Elixir
Tags: raspberry-pi,elixir

Elixir is a modern, functional programming language, based on the Erlang runtime
environment. Erlang has a long history of being a robust platform for building
distributed systems with many concurrent "processes" that run concurrently. The
processes in quotation marks means light-weight processing containers managed by
the BEAM (the Erlang runtime virtual machine).

During the last months I've dabbled a bit with Elixir, mostly from following the
excellent book by Dave Thomas: "Programming Elixir". By the way, the book will
soon be updated for Elixir version 1.6.

Since PI day is coming up (3/14 in U.S. date format), I thought it would be a
fun way to explore using Elixir's concurrent processing to calculate some digits
of the number pi!  On the topic of "pi", why not use some Raspberry PIs ;-)

# Nodes on the network

My setup is four Raspberry Pi 3 devices. These four Raspberry Pis will each
run an instance of the BEAM (the Erlang VM), and these VM instances are called
"nodes". When these nodes have a name, they can connect to other named nodes.
Once connected, the nodes can send messages to processes running on other nodes.
Apart from the four Raspberry Pi nodes, there one more node in my setup: the
master node that i have running on my laptop. This master node keeps track of
the work to be done and distributes work packets to the worker nodes.

The graphic below illustrates the idea for work distribution:

# The Raspberry PIs

The company i work for (PMA Solutions) recently had a developer challenge, kind
of an internal hackathon, in which each team had to build a voice-interface
using Raspberry PI devices. So i could borrow two Raspberry Pis and with two of
my own I have a little stack of four devices connected to the local network via
Ethernet cables to a switch mounter under the desk:

![stack]({filename}/extras/rpi-stack.JPG)

Each device is the Raspberry Pi model B, having a 1.2 GHz 64-bit CPU which is
rather slow, but four cores that can come in handy for concurrent computation.

Running the final program on the Raspberry Pis shot up the temperature upward of
80 °C. For any long periods of calculation this cannot be good for the life of
the chips so I put some heatsinks on the chips:

![heatsink]({filename}/extras/rpi-heatsink.JPG)

The heatsinks really makes a difference. Without the heatsinks, the idle
temperature was about 45°C and with heatsink it came down to 42°C. During full
load, the temperature could be held between 50°C and 60°C with the help of some
fans, as in the picture below:

![fan setup]({filename}/extras/rpi-fan-setup.JPG)

# Formula for calculating Pi

When one starts to look into formulas for Pi, one enters a fascinating world of
mathematics. There are several formulas that are based on a summation of a
series of terms. In this exercise, the
[Bailey–Borwein–Plouffe](https://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula) formula was used:

![BBP Formula](https://wikimedia.org/api/rest_v1/media/math/render/svg/af6bc360851499dd2ab2a90bee03fbe2040089d5)

Each term in this sum represents a digit in the nth digit position. Although,
the digit position is not a decimal position, it is a hexadecimal position. For
the sum, it makes no difference. The series can be broken up into "chunks" that
can be assigned as work packets for the worker nodes.

# Some background on Elixir/Erlang processes

Before going further with the Elixir implementation, here is a high-level
overview of processes in Elixir/Erlang. Erlang uses processes to isolate units
of processing, allowing concurrent programming. Processes do not expose their
state and the way they interact with other processes is by passing messages to
another process.

When spawning a new Elixir/Erlang process, the result is a PID - a process
identifier. Other processes can then send messages to this PID.

Here is an example, a module that keeps track of a count, that can be
incremented or decremented:

    :::Elixir:::
    defmodule Counter do
        def start(initial_value) do
            spawn fn -> count(initial_value) end
        end

        def count(current_value) do
            receive do
            {:add, number}      ->  count(current_value + number)
            {:subtract, number} ->  count(current_value - number)
            {:value, sender}    ->  send(sender, current_value)
                                    count(current_value)
            end
        end
    end

Calling the `start` method spawns a new process using the `spawn` function that
takes one argument: a function to run. In this case, the anonymous function
calls the `count` function that will wait for messages to be received.

The `count` function contains a `receive do` block. It will match an incoming
message value and act on it. In each of the three types of messages,
the count function calls itself again. This is often called a "receive loop"
because the function will keep on listening for new messages and respond to
them. Note: this is not your typical recursion that creates a new call stack.
Elixir uses "tail call optimization" when the recursive call to the same
function happens as the last statement. In that case the call stack is not kept
around when the function is called again, so there is no stack overflow.

Elixir does not have the concept of objects that carry state with them. In this
case we do want to keep track of the counter value. The state is passed to the
count function as an argument.

Below is a sample of how the above Counter module can be used:

    :::Elixir:::
    # Create a new Counter process, and initialize the counter to 10:
    pid = Counter.start(10)

    # Add 5 and subtract 3 from the counter by sending messages to
    # the process's pid
    send(pid, {:add, 5})
    send(pid, {:subtract, 3})

    # Finally, send a message to retrieve the value of the counter.
    # Here we send the current process's pid (the call to self()), and that way
    # the Counter can send back the value
    send(pid, {:value, self()})

    # Finally, receive the message with the value:
    receive do
        value -> IO.puts "The value is #{value}"
    end

Erlang comes with a whole framework for managing processes, called OTP - the
Open Telecom Platform. One of the constructs that encapsulates the process
communication and message passing is the GenServer, a generic server that can
respond to synchronous and asynchronous calls. For each type of call, the
GenServer manages the state. It takes care of the receive loops. The Counter can
be written as follows to be a GenServer:

    :::Elixir:::
    defmodule Counter do
        use GenServer

        def handle_cast({:add, number}, current_value) do
            # Cast does not have a reply. State changes by adding number:
            {:noreply, current_value + number}
        end

        def handle_cast({:subtract, number}, current_value) do
            # Cast does not have a reply. State changes by subtracting number:
            {:noreply, current_value - number}
        end

        def handle_call(:value, _from, current_value) do
            # A call is synchronous and returns a value.
            # The three-part tuple below indicates that
            # - a value is to be returned
            # - the return value is `current_value`
            # - the state of the GenServer is `current_value` (unchanged)
            {:reply, current_value, current_value}
        end
    end

In this example, the Counter GenServer accepts "cast" (asynchronous) and "call"
(synchronous) invocations. The above example has two `handle_cast` function
definitions. One of these two will be called, based on pattern matching the
first argument. The `handle_cast` function is a callback that Elixir will call
when it receives a `GenServer.cast` function call. Similarly, there is a
`handle_call` callback defined that will handle calls to `GenServer.call`. The
difference between `GenServer.cast` and `GenServer.call` is that a cast is
asynchronous - it does not return a value to the caller - hence the `:noreply`
atom. The call on the other hand is synchronous and returns a value.

Here is an example of using the Counter as a GenServer:

    :::Elixir:::
    # Create a new Counter GenServer, and initialize the counter to 10:
    {:ok, pid} = GenServer.start_link(Counter, 10)

    # Add five and subtract 3 from the counter by sending messages to
    # the process's pid
    GenServer.cast(pid, {:add, 5})
    GenServer.cast(pid, {:subtract, 3})
    value = GenServer.call(pid, :value)
    IO.puts "The value is #{value}"

# The master node

One node is designated the "master node". It runs a GenServer that defines a
list of digit positions from 0 to 10000, and keeps track of the value of pi
computed so far.

Here is the Elixirpi.Collector module, somewhat simplified compared to the
version on [GitHub](https://github.com/pythonquick/elixirpi):

    defmodule Elixirpi.Collector do
        use GenServer
        alias Decimal, as: D
        @digit_batch_size 8
        @target_hex_digits 10000
        @precision div(@target_hex_digits * 4, 3)

        def start do
            digit_positions = Enum.reduce(@target_hex_digits..0, [], &([&1 | &2]))
            pi = D.new(0) # Initial value
            {:ok, pid} = GenServer.start_link(__MODULE__, {pi, digit_positions})
            :global.register_name(:collector_process_name, pid)

            # Serve worker requests - do not exit
            :timer.sleep(:infinity)
        end

        ##############################################################################
        # GenServer callbacks
        ##############################################################################

        def handle_call(:next_digit_positions, _from, {pi, digit_positions}) do
            {next_digits, remaining}  = Enum.split(digit_positions, @digit_batch_size)
            output_progress(next_digits, pi)
            {:reply, {next_digits}, {pi, remaining}}
        end

        def handle_cast({:update_pi, additional_term}, {pi, digit_positions}) do
            D.set_context(%D.Context{D.get_context | precision: @precision}) 
            updated_pi = D.add(pi, additional_term)
            {:noreply, {updated_pi, digit_positions}}
        end

        # ... a few more private methods omited
    end

In the `start` function, the `Enum.reduce` function takes each item of the range
(10000..0) and successively adds it to the accumulator construct, which is
initially the empty list: []:

    :::Elixir:::
    digit_positions = Enum.reduce(@target_hex_digits..0, [], &([&1 | &2]))

This results in a list of integer values from 0 up to 10000 inclusive. 

The server process is created in the following line using the function
`GenServer.start_link`. Here we initialize the state of the GenServer with three
items:

* the value of pi calculated so far
* the list of digit positions for the number pi to be calculated, 

Note: the PID of the master node is registered in a global registry:

    :::Elixir:::
    :global.register_name(:collector_process_name, pid)

This way, other nodes can look up the PID of the master node, even if they are
on a different host on the network.


# The worker node

When each worker node starts up, it keeps asking the master node for more digits
to calculate. It calculates the digit positions in parallel task processes, and
sends back the results to the master node.

Here is a simplified module listing of the worker node:

    :::Elixir:::
    defmodule Elixirpi.Worker do
        alias Elixirpi.Collector
        alias Decimal, as: D

        # Commonly used formula constants:
        @d1 D.new(1)
        @d2 D.new(2)
        @d4 D.new(4)
        @d5 D.new(5)
        @d6 D.new(6)
        @d8 D.new(8)
        @d16 D.new(16)

        def term(digit_position, sixteen_power) do
            digit_position_decimal = D.new(digit_position)
            eight_times_digit_pos = D.mult(@d8, digit_position_decimal)
            D.div(@d4, eight_times_digit_pos |> D.add(@d1))
            |> D.sub(D.div(@d2, eight_times_digit_pos |> D.add(@d4)))
            |> D.sub(D.div(@d1, eight_times_digit_pos |> D.add(@d5)))
            |> D.sub(D.div(@d1, eight_times_digit_pos |> D.add(@d6)))
            |> D.div(sixteen_power)
        end

        def process_next_digits(precision) do
            D.set_context(%D.Context{D.get_context | precision: precision})
            next_digit_positions = GenServer.call(master_node_pid(), :next_digit_positions)

            # Calculate each digit term in concurrent stream of Tasks:
            Task.async_stream(next_digit_positions, fn digit_position ->
                D.set_context(%D.Context{D.get_context | precision: precision})
                sixteen_power = calc_sixteen_power(digit_position)
                term(digit_position, sixteen_power)}
            end, timeout: 100000)
            |> Enum.each(fn {:ok, next_term} ->
                GenServer.cast(master_node_pid(), {:update_pi, next_term})
            end)

            next_digit_positions
        end

        def keep_processing_digits(precision) do
            next_digit_positions = process_next_digits(precision)
            case next_digit_positions do
                [] -> IO.puts "Worker finished"
                _ -> keep_processing_digits(precision)
            end
        end

        def run() do
            precision = Collector.precision
            keep_processing_digits(precision)
        end

        # ... a few more private methods omited

    end


In the `process_next_digits` function, it fetches the next chunk of digit
positions to calculate. Then, for each digit position, call `Task.async_stream` to spawn
a Task. A task is a process that runs a function in the background. Each task calculates
a digit of pi using the `term` function using the Bailey–Borwein–Plouffe formula
mentioned above.

Finally, each of the task results are collected, and the result sent to the
master node.

# The Result

The result of running the four Raspberry Pi nodes for two hours is the generated
file pi.txt with 10000 decimal digits. 

The goal was by no means to break any records with this. It is a fun way to
explore Elixir's (and Erlang's) programming model and how processes and nodes
can be distributed across the network to work with each other.

A next step can be to try a formula that converges faster to the value of pi

