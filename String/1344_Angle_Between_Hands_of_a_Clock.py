""" Given two numbers, hour and minutes, return the smaller angle (in degrees) formed between the hour and the minute
hand. """


def angle_clock(hour, minutes):
    """ The idea is to calculate separately the angles between 0-minutes vertical line and each hand. The answer is
        the difference between these two angles.
        Let's start from the minute hand. The whole circle is equal to 360° or 60 minutes, i.e. minute hand moves
        1 min = 360°/60 = 6° at each minute. Now we could easily find the angle between 0-minutes vertical line and a
        minute hand:
            minutes_angle = minutes × 6°
        Similarly with the minute hand angle, the whole circle is equal to 360° or 12 hours, hence for each hour, the
        hour hand moves 1h = 360°/12 = 30°. Now we could easily find an angle between 12-hour vertical line and an
        hour hand:
            hour_angle = hour × 30°
        Note that for 12-hour the actual angle is zero, therefore the expression has to be corrected:
            hour_angle = (hour mod 12) × 30°
        In a more general case where minutes > 0, we have to take into account an additional movement of hour hand:
        It doesn't jump between the integer values but follows the movement of minute hand as well.
        Since, for every 60 minutes, our hour hand rotates by 30°, so for every minute it is rotated by 30°/60 = 0.5°
        Therefore:
            hour_angle = (hour mod 12) × 30° + minutes x 0.5°
        We finally ind the difference:
            angle = abs(hour_angle - minutes_angle)
        and return the smallest angle:
            min(angle, 360 - angle)
    Time complexity: O(1)
    Space complexity: O(1)
    """
    minutes_hand = minutes * 6
    hours_hand = (hour % 12) * 30 + minutes * 0.5
    angle = abs(minutes_hand - hours_hand)
    return min(angle, 360 - angle)
