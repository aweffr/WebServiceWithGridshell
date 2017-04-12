def input_to_array(s):
    out = []
    try:
        points = s.split()
        for p in points:
            tmp = p.strip().strip("()").split(",")
            out.append(map(float, tmp))
        return out
    except Exception as e:
        print e
        return False