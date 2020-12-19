import pymunk as pm


class Body():

    def __init__(self, position, mass, moment, body_type=pm.Body.DYNAMIC):

        self.body = pm.Body(mass=mass, moment=moment, body_type=body_type)
        self.body.position = position

    def set_position(self, x, y):

        self.body.position = x, y


class Ball(Body):

    def __init__(self, *, position, collision_type, radius, mass):

        moment = pm.moment_for_circle(
            mass=mass, inner_radius=radius, outer_radius=radius)
        Body.__init__(self, position, mass, moment)

        self.shape = pm.Circle(self.body, radius)
        self.shape.elasticity = 0.5
        self.shape.friction = 1
        self.shape.density = .999
        self.shape.collision_type = collision_type

        setattr(self.shape, "touches", 0)


class Stick(Body):

    def __init__(self, *, position, collision_type, radius, mass):

        moment = pm.moment_for_circle(
            mass=mass, inner_radius=radius, outer_radius=radius)
        Body.__init__(self, position, mass, moment, pm.Body.KINEMATIC)

        self.shape = pm.Circle(self.body, radius)
        self.shape.elasticity = 1
        self.shape.collision_type = collision_type


def post_solve_stick_ball(arbiter, space, _):
    shape, _ = arbiter.shapes

    if shape.touches < 2:
        shape.body.apply_impulse_at_local_point((0, -100000), (0, 0))
        shape.touches += 1


def post_solve_segment_ball(arbiter, space, _):
    shape, _ = arbiter.shapes

    if shape.touches > 0:
        shape.touches -= 1
