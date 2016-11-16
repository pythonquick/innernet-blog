Title: CSS Debugging
Date: 2015-12-22
Category: Tutorials
Tags: CSS

This is a recap of a recent tutorial about CSS and the Chrome Inspector at my company.

We showed the Chrome Inspector's "Elements" tab to inspect CSS styles for selected tags on the page.

The following screenshots illustrate a few features of the inspector

# One option: inspect higher-level elements

Let's say you want to change a CSS style or override it with a different style. The current style could be defined on a parent element and gets inherited down, or it could be applied to a  child element. 

How do you know where the style is defined? One way is to try to override the style by applying a style value directly to a parent element using the Chrome Inspector. Inspect the parent tag and it will show the styles in the "style" panel. There you can add a style rule to the top section of the panel under the area "Element". If that doesn't result in a visible change on the page, apply the style to the next-lower child element until you find the element where the CSS attribute change shows up on the page.

The screenshot below shows the `color` style that got overridden to blue. On parent elements, the color setting had no effect to the text color on the page, but on the `a` tag, the color finally changed. That means, the original orange style color on the page must have been applied to the `a` tag. Now inspect the style rules on this `a` tag and find which CSS rule applies the original orange color. Now you know which style to change or override.

![find element for style](https://innernet.io/media/find-element-for-style.png)

# Another option: Inspect lowest-level element

Another approach is to look at the lowest-level element - the element that directly displays the item on the screen.

For example, if you have an orange text label and you want to know where the orange style comes from, inspect the `span` / `label` tag that displays the text. Then look at its style definition in the Chrome Inspector's Style tag. If the style is not applied to the span / label element, it might be inherited from a parent element. In that case, Chrome will indicate inherited styles by the label "Inherited from". The screenshot below shows that the orange color is inherited from a parent `a` element that has the CSS class `ui-link-inherit` that in turn has a parent element with the class `ui-btn-up-c`

![find element for style](https://innernet.io/media/find-element-for-style2.png)


