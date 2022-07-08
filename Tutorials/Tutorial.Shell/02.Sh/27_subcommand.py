from sh import git

# resolves to "git branch -v"
v1 = git.branch("-v")
v2 = git("branch", "-v")

# print(v1)
# print(v2)
