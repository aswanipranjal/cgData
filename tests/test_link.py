#!/usr/bin/env python

import unittest
import os

import CGData
import CGData.DataSet

CGData.LOG_LEVEL=0
class TestCase(unittest.TestCase):
    def test_load(self):
        
        ds = CGData.DataSet.DataSet()
        ds.scan_dirs( ["data_link2/"] )
        
        fileTypes = ds.get_file_types()
        assert "genomicMatrix" in fileTypes
        assert "clinicalMatrix" in fileTypes
        
        mapTypes = ds.get_map_types()
        print mapTypes
        assert "probe" in mapTypes
        
        ms = ds['genomicMatrix']['test'].get_link_map()
        assert "rowKeyMap" in ms
        assert "columnKeyMap" in ms
        
        ms = ds.query(dst_type='id', src_type='genomicMatrix')
        assert len(ms) == 1
        assert ms[0].src_name == "test"
        assert ms[0].src_type == "genomicMatrix"        
        assert ms[0].predicate == "columnKeyMap"        
        assert ms[0].dst_type == "id"
        assert ms[0].dst_name == "test"
        
        ms = ds.query(dst_type='id', predicate='rowKeyMap')
        assert len(ms) == 1
        assert ms[0].dst_name == "test"
        assert ms[0].dst_type == "id"        
        assert ms[0].predicate == "rowKeyMap"        
        assert ms[0].src_type == "clinicalMatrix"
        assert ms[0].src_name == "test"


def main():
    sys.argv = sys.argv[:1]
    unittest.main()

if __name__ == '__main__':
    main()
