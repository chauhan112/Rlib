from lib import Solver
class Main:
    def solve(path_to_inp_file: str, outfile: str =None):
        s = Solver()
        s.set_input_file(path_to_inp_file)
        if outfile is None:
            return s.solve()
        s._out_txt = outfile
        s.write_output()