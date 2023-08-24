# CI

### How to create docker images automatically

- `git tag -a 0.0.1 -m "Test docker build with GH actions"`
- `git push origin 0.0.1`
- And check actions: https://github.com/mrceyhun/ppdgui/actions

### How to migrate another repository

- You've to create `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` in the GH repo settings
- Change your docker hub image name whatever you want instead of `mrceyhun/ppdgui`. Beware that `mrceyhun` is my docker hub username.
