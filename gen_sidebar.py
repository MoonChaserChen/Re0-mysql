import os

suffix = ".md"
gen_file = "_sidebar.md"


def print_file(c_dir, depth, write2):
    for f in os.listdir(c_dir):
        re_f = os.path.join(c_dir, f)
        is_d = os.path.isdir(re_f)
        if(is_d):
            write2.write("\t" * depth + "- " + f + "\n")
            print_file(re_f, depth + 1, write2)
        else:
            if (suffix in f and gen_file not in f):
                f_n = os.path.splitext(f)[0]
                write2.write("\t" * depth + "- [" + f_n + "](/" + re_f + ")\n")


with open(gen_file, 'w') as g_f:
    print_file(".", 0, g_f)
