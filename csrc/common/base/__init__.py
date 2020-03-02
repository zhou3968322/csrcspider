# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/3/1
import json, os, abc, codecs
from csrc.settings import META_DIR


class MonthMetaItemWriterPipeline(object):
    
    def __init__(self):
        self.md5_dict = {}
        self.file_dict = {}
        self._dump_fields = []
        self._md5_suffix = "_meta_md5.txt"
        self._meta_suffix = "_meta.txt"
    
    def _get_fo(self, month_str):
        if month_str in self.file_dict:
            return self.file_dict[month_str]
        month_dir = os.path.join(META_DIR, month_str)
        if not os.path.isdir(month_dir):
            os.mkdir(month_dir)
        meta_path = os.path.join(month_dir, "{}{}".format(month_str, self._meta_suffix))
        if not os.path.isfile(meta_path):
            fo = codecs.open(meta_path, "w", "utf-8")
        else:
            fo = codecs.open(meta_path, "a", "utf-8")
        self.file_dict[month_str] = fo
        return fo
    
    def _update_md5(self, month_str, md5):
        if month_str not in self.md5_dict:
            self.md5_dict[month_str] = [md5]
        else:
            self.md5_dict[month_str].append(md5)
    
    def _dump(self, item):
        out_data = {}
        for key in item.keys():
            if key in self._dump_fields:
                out_data[key] = item[key]
        return json.dumps(out_data, ensure_ascii=False)
    
    @abc.abstractmethod
    def process_item(self, item, spider):
        pass
    
    def close_spider(self, spider):
        assert set(self.md5_dict.keys()) == set(self.file_dict.keys())
        for month_str in self.md5_dict.keys():
            month_dir = os.path.join(META_DIR, month_str)
            if not os.path.isdir(month_dir):
                os.mkdir(month_dir)
            meta_md5_path = os.path.join(month_dir, "{}{}".format(month_str, self._md5_suffix))
            if os.path.isfile(meta_md5_path):
                with codecs.open(meta_md5_path, 'r', 'utf-8') as fr:
                    old_meta_md5_list = fr.read().splitlines()
                md5_set = set(old_meta_md5_list + self.md5_dict[month_str])
            else:
                md5_set = set(self.md5_dict[month_str])
            with codecs.open(meta_md5_path, 'w', 'utf-8') as fw:
                fw.write('\n'.join(md5_set))
            self.file_dict[month_str].close()
