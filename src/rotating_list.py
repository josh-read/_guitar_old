class RotatingList(list):
    """List with a rotation parameter, which applies an offset when iterating through the list.

    The end result is similar to using the collections.deque rotate method, however the original order
    can be retrieved by setting rotation to zero."""

    def __init__(self, *args, rotation=0, **kwargs):
        super(RotatingList, self).__init__(*args, **kwargs)
        self.rotation = rotation

    def __iter__(self):
        rotated_list = self[self.rotation:] + self[:self.rotation]
        return iter(rotated_list)

    def rotate(self, n=1):
        self.rotation += n
