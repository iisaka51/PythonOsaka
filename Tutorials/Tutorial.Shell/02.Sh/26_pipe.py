from sh import sort, du, wc, ls
# df -sb /tmp | sort -rn
print(sort(du("-s", "/tmp"), "-rn"))

# ls -l /etc | wc -l
print(wc(ls("-1", "/etc"), "-l"))
