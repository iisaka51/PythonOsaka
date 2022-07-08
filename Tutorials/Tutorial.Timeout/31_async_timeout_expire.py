sync with timeout(1.5) as cm:
    await inner()
    print(cm.expired)
