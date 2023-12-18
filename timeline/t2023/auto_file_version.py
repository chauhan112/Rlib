import os
import shutil
import datetime

class VersionModel:
    def set_file_path(self, file_path):
        self._path = file_path.replace(os.sep, "/")
        if not os.path.exists(self._path):
            SerializationDB.pickleOut({}, self._path)
        self._content = SerializationDB.readPickle(file_path)
    def get_file_key_name(self, path):
        abspath = os.path.abspath(path)
        return abspath.replace(os.sep, "/")
    def set_storage_path(self, storage_folder):
        self._storage = storage_folder
        self._data_path = self._storage + "/" + "data"
        if not os.path.exists(self._data_path):
            os.makedirs(self._data_path)
        self.set_file_path(storage_folder + "/" + "_index.pkl")
    def get_next_count(self, file_path):
        edited = False
        key = self.get_file_key_name(file_path)
        if "data" not in self._content:
            self._content['data'] = {}
            edited = True
        if key not in self._content['data']:
            self._content['data'][key] = {'current': 0, 
                                          'versions': {'times': {}, 'order': []}, 
                                          "uuid": CryptsDB.generateRandomName(),
                                          'total': 0
                                          }
            edited = True
        if edited:
            self._write()
        return self._content['data'][key]['current'] + 1
    def set_counts(self, total_count, count_per_day):
        self._content["total_count"] = total_count
        self._content["count_per_day"] = count_per_day
        self._write()
    def _write(self):
        SerializationDB.pickleOut(self._content, self._path)
    def update_count(self, file, countNr):
        key = self.get_file_key_name(file)
        allInfo = self._content['data'][key]
        vs = allInfo['versions']
        todayStamp = TimeDB.getTimeStamp()
        if todayStamp  not in vs['times']:
            vs['times'][todayStamp] = []
            vs['order'].append(todayStamp)
        arr = vs['times'][todayStamp]
        if len(arr) < self._content["count_per_day"]:
            arr.append(countNr)
            allInfo['total'] += 1
        else:
            while len(arr) > self._content["count_per_day"] - 1:
                arr.pop(0)
            arr.append(countNr)
        self._remove_extra(key)
        allInfo['current'] = countNr
        self._write()
    def _remove_extra(self, key):
        allInfo = self._content['data'][key]
        vs = allInfo['versions']
        while allInfo['total'] > self._content["total_count"]:
            firstTimeStamp = vs['order'][0]
            vs['times'][firstTimeStamp].pop(0)
            allInfo['total'] -= 1
            if len(vs['times'][firstTimeStamp] ) == 0:
                del vs['times'][firstTimeStamp]
    def get_id_name(self, file_path):
        self.get_next_count(file_path)
        key = self.get_file_key_name(file_path)
        return self._content['data'][key]['uuid']
    def reset(self):
        self._content = {}
        self._write()
    def get_name(self, file_path, nr):
        key = self.get_file_key_name(file_path)
        basename = os.path.basename(file_path)
        allInfo = self._content['data'][key]
        idd = allInfo['uuid']
        return f"{self._storage}/data/{idd}{nr}-{basename}"
    def get_file_data(self, file_path):
        key = self.get_file_key_name(file_path)
        if 'data' not in self._content:
            self.get_next_count(file_path)
        return self._content['data'][key]
class FileNameCountManager:
    def __init__(self) -> None:
        self._file_ops = FileOperation()
    def set_model(self, model: VersionModel):
        self._model = model
        self._all_files = Path.getFiles(model._data_path)
    def restore(self, file_path, nr):
        basename = os.path.basename(file_path)
        nmae = self._model.get_name(file_path, nr)
        self._file_ops.set_file(nmae)
        dirname= os.path.dirname(file_path)
        if dirname == "":
            dirname = "."
        self._file_ops.copy(dirname, basename)
        self._update_size(file_path)
    def make_version(self, file_path):
        if self.has_changed(file_path):
            nr = self._model.get_next_count(file_path)
            new_name = self._model.get_name(file_path, nr)
            self._file_ops.copy(self._model._data_path, os.path.basename(new_name))
            self._model.update_count(file_path, nr)
            self._update_size(file_path)
            print("versioned")
            files_to_delete = self._get_all_extra_files_to_delete(file_path)
            if len(files_to_delete) >0:
                File.deleteFiles(files_to_delete)
    def _update_size(self, file_path):
        data = self._model.get_file_data(file_path)
        data["last_size"] = self._file_ops.get_size()
        self._model._write()
    def has_changed(self, file_path):
        self._file_ops.set_file(file_path)
        data = self._model.get_file_data(file_path)
        if "last_size" in data:
            return data['last_size'] != self._file_ops.get_size()
        return True
    def _get_all_extra_files_to_delete(self, file_path):
        data = self._model.get_file_data(file_path)
        vs = data['versions']['times']
        ids =set()
        for datestp in vs:
            vals = vs[datestp]
            for v in vals:
                ids.add(v)
        files = os.listdir(self._model._data_path)
        current_files = filter(lambda x: data['uuid'] in x, files)
        basenmae = os.path.basename(file_path)
        nums = set(map(lambda x: int(x.replace(data['uuid'],"").replace("-"+basenmae, "")), current_files))
        rems = nums.difference(ids)
        todel = map(lambda x: self._model.get_name(file_path, x), rems)
        return list(todel)
class FileOperation:
    def set_file(self, file_path):
        self._file_path = file_path

    def rename(self, new_name):
        directory_path = os.path.dirname(self._file_path)
        new_file_path = os.path.join(directory_path, new_name)
        os.rename(self._file_path, new_file_path)
        self._file_path = new_file_path
        
    def move(self, new_path, new_name=None):
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        if new_name is None:
            new_name = os.path.basename(self._file_path)
        new_file_path = os.path.join(new_path, new_name)
        shutil.move(self._file_path, new_file_path)
        self._file_path = new_file_path
        
    def get_size(self):
        file_size = os.path.getsize(self._file_path)
        return file_size
        
    def get_last_modified_date(self):
        timestamp = os.path.getmtime(self._file_path)
        last_modified_date = datetime.datetime.fromtimestamp(timestamp)
        return last_modified_date
        
    def copy(self, destination_path, new_name = None):
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        if new_name is None:
            new_name = os.path.basename(self._file_path)
        destination_file_path = os.path.join(destination_path, new_name)
        shutil.copy(self._file_path, destination_file_path)
class AutoVersionSystem:
    pass