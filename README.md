# Basic Flask/Angular template

This is the world's least-featured MVC application, supporting exactly one REST
endpoint and barely any UI. That said, I think it would make a decent starting
point to build out a web app.

Other things it lacks:

- Dependency management: There's zero tooling set up on the frontend; Bootstrap
  and Angular are statically-linked (copied directly into the source tree). The
  backend is slightly better, but it depends on four libraries which you're
  expected to have installed yourself. Mostly because I don't know how
  virtualenv works.
- User management or authentication
