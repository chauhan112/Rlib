#https://codingcompetitions.withgoogle.com/codejam/round/0000000000877b42/0000000000afe6a1
import os
from FileDatabase import File
class IMerger:
    def get_merged_string(self):
        pass
    def set_towers(self):
        pass
class ITowerValidity:
    def check(self):
        pass
class ChallengeReader:
    def __init__(self):
        self._test_cases = []
    def set_file(self, file:str):
        self._path = file
        self.set_content(File.getFileContent(file))
    def set_content(self, content: str):
        lines = content.splitlines()
        for i in range(1, len(lines), 2):
            self._test_cases.append(lines[i+1].split())
    def get_cases(self):
        return self._test_cases
class FrequencyCount:
    def set_string(self, word:str):
        self._word = word
    def execute(self):
        res = {}
        for l in self._word:
            if l in res:
                res[l] += 1
            else:
                res[l] = 1
        return res
class EndPosition:
    def set_word(self, word: str):
        self._word = word
    def get_end_positions(self, letter: str):
        first =last = None
        for i, l in enumerate(self._word):
            if l == letter:
                first = i
                break
        for i in range(len(self._word)-1, -1, -1):
            l = self._word[i]
            if l == letter:
                last = i
                break
        return first, last
class SingleTowerValidity(ITowerValidity):
    def set_tower(self, tower: str):
        self._tower = tower
    def check(self):
        ep = EndPosition()
        ep.set_word(self._tower)
        fc = FrequencyCount()
        fc.set_string(self._tower)
        freq = fc.execute()
        for l in freq:
            if freq[l] > 1:
                a, b = ep.get_end_positions(l)
                if len(set(self._tower[a:b+1])) > 1:
                    return False
        return True
class ManyTowersCombinedChecker(ITowerValidity):
    def __init__(self):
        self._sol = None
        self.set_merger(MergerForCyclicWords())
    def set_towers(self, tower: list):
        self._towers = tower
    def check(self):
        stv = SingleTowerValidity()
        all_check = True
        for tower in self._towers:
            stv.set_tower(tower)
            all_check = all_check and stv.check()
        if not all_check:
            return False
        mr = self._merger
        mr.set_towers(self._towers)
        sol = mr.get_merged_string()
        if len(sol) != len("".join(self._towers)):
            return False
        stv.set_tower(sol)
        self._sol = sol
        return stv.check()
    def get_solution(self):
        return self._sol
    def set_merger(self, merger: IMerger):
        self._merger = merger
class MBlock:
    def __init__(self, val: str):
        self.next = None
        self.before = None
        self.value = val
    def addable_before(self, val: str):
        if self.value == "":
            return True
        return val[-1] == self.value[0]
    def addable_after(self, val: str):
        if self.value == "":
            return True
        return val[0] == self.value[-1]
    def add_before(self, val: str):
        self.value = val + self.value
    def add_after(self, val: str):
        self.value += val
class Merger(IMerger):
    def __init__(self):
        self._str_stars_with = "starts_with"
        self._str_ends_with = "ends_with"
        self._blocks = {}
    def set_towers(self, towers: list[str]):
        self._towers = towers
    def _merged_blocks(self):
        st, en = self._make_mapper().values()
        a, b = st.copy(), en.copy()
        inter = set(a).intersection(set(b))
        for c in inter:
            va = a[c].pop()
            vb = b[c].pop()
            ma = self._get_block(va)
            mb = self._get_block(vb)
            if ma != mb:
                ma.before = mb
                mb.after = ma
        return self._blocks
    def _get_block(self, val):
        if val not in self._blocks:
            self._blocks[val] = MBlock(val)
        return self._blocks[val]
    def _make_mapper(self):
        ampper = {self._str_stars_with:{}, self._str_ends_with:{}}
        def add(wo, dic, l ):
            if l in dic:
                dic[l].append(wo)
            else:
                dic[l] = [wo]

        for word in self._towers:
            s = word[0]
            e = word[-1]
            add(word, ampper[self._str_stars_with], s)
            add(word, ampper[self._str_ends_with], e)
        return ampper
    def get_merged_string(self):
        self._merged_blocks()
        res = ""
        visited = set()
        for c in self._blocks:
            node = self._blocks[c]
            if node.value not in visited:
                string, v = self._merge(node)
                res += string
                visited = visited.union(v)
        return res
    def _merge(self, node):
        res = ""
        visited = set([node.value])
        p = node
        while True:
            res = p.value + res
            visited.add(p.value)
            if p.before is None or p.before.value in visited:
                break
            p = p.before
        p = node
        while True:
            if p.next is None or p.before.value in visited:
                break
            p = p.next
            res += p.value
            visited.add(p.value)
        return res, visited
class Solver:
    def __init__(self):
        self.set_combined_tower_check(ManyTowersCombinedChecker())
        self._out_txt = "out.txt"
    def set_combined_tower_check(self, checker: ManyTowersCombinedChecker):
        self._checker =checker
    def set_towers(self, towers: list[list[str]]):
        self._towers_list = towers
    def set_input_file(self, file: str):
        self._cr = ChallengeReader()
        self._cr.set_file(file)
        self.set_towers(self._cr.get_cases())
        self._out_txt= file.replace("input.txt", "_mine_output.txt")
    def solve(self):
        res = []
        cp = self._checker
        for towers in self._towers_list:
            cp.set_towers(towers)
            is_solvable = cp.check()
            if is_solvable:
                res.append(cp.get_solution())
            else:
                res.append("IMPOSSIBLE")
        return res
    def write_output(self, arr=None):
        if arr is None:
            arr = self.solve()
        res = ""
        for i in range(len(arr)):
            res += f"Case #{i+1}: {arr[i]}\n"
        File.createFile(self._out_txt, res)
class MergerForCyclicWords(IMerger):
    def set_towers(self, towers: list[str]):
        self._towers = towers
    def _try_merging(self, arr: list):
        if len(arr) == 1:
            return arr
        towers = arr.copy()
        res = [MBlock2()]
        while True:
            b = towers.pop()
            added = False
            for tb in res:
                if tb.can_be_added(b):
                    tb.add(b)
                    added = True
                    break
            if not added:
                block = MBlock2()
                block.add_right(b)
                res.append(block)
            if len(towers) == 0:
                break
        return self._merge_blocks(res)

    def _merge_blocks(self, blocks):
        if len(blocks) == 1:
            return blocks
        c = 0
        while True:
            if len(blocks) == 0:
                break
            b = blocks.pop()
            adedd = False
            for tb in blocks:
                if tb.can_be_added(b.value):
                    tb.add(b.value)
                    adedd = True
                    c=0
                    break
            if not adedd:
                c += 1
                blocks.insert(0, b)
            if c == len(blocks):
                break
        return blocks

    def get_merged_string(self):
        res = self._try_merging(self._towers)
        return "".join([x.value for x in res])
class MBlock2:
    def __init__(self) -> None:
        self._values = []
        self.before = None
        self.next = None
    def can_be_added(self, val: str):
        self._added = (False, None)
        for i in range(1, len(self._values)):
            left, right = self._values[i-1], self._values[i]
            if left[-1] == val[0] and right[0] == val[-1]:
                self._added = (True, i)
                break
        if len(self._values) == 0:
            self._added = (True, "before")
        elif not self._added[0]:
            if self._values[0][0] == val[-1]:
                self._added = (True, "before")
            elif self._values[-1][-1] == val[0]:
                self._added = (True, "after")
        return self._added[0]

    def add_left(self, val: str):
        self._values.insert(0, val)
    def add_right(self, val: str):
        self._values.append(val)
    def add(self, val: str):
        addable, index = self._added
        if addable:
            if type(index) == int:
                self._values.insert(index, val)
            elif index == "before":
                self.add_left(val)
            elif index == "after":
                self.add_right(val)
        else:
            raise IOError("value cannot be added")
    @property
    def value(self):
        return "".join(self._values)