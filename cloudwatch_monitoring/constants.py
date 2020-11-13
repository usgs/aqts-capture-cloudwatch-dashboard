"""
module for creating generic constants used by multiple modules

"""
"""
    The cloudwatch dashboard grid positioning system will automatically set x and y coordinates of every widget
    in the list, based on the next available x,y on the dashboard, from left to right, then top to bottom.  As long
    as we specify height and width, and are ok with this default positioning behavior, positioning can be as simple
    as specifying the height and width of the widget.
    doc: https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html#CloudWatch-Dashboard-Properties-Widgets-Structure
"""
positioning = {
    'width': 24,
    'height': 3
}
