"""
module for keeping track of widget position on the dashboard

"""


class Positioning:
    """
        The cloudwatch dashboard grid positioning system will automatically set x and y coordinates of every widget
        in the list, based on the next available x,y on the dashboard, from left to right, then top to bottom.  As long
        as we specify height and width, and are ok with this default positioning behavior, positioning can be as simple
        as specifying the height and width of the widget.

        doc: https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html#CloudWatch-Dashboard-Properties-Widgets-Structure
    """
    def __init__(self):
        self.width = 24
        self.height = 3
