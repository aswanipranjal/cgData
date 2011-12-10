import unittest
import os

import subprocess
import shutil
import MySQLdb
import MySQLSandbox

class TestCase(unittest.TestCase):
    """Test sample ordering in output tables"""
    tolerance = 0.001 # floating point tolerance

    @classmethod
    def setUpClass(cls):
        try:
            shutil.rmtree('out')
        except:
            pass
        cls.sandbox = MySQLSandbox.Sandbox()
        db = MySQLdb.connect(read_default_file=cls.sandbox.defaults)
        cls.c = db.cursor()
        # create raDb and hg18
        cls.c.execute("""
create database hg18;
use hg18;

CREATE TABLE colDb (
    `id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name varchar(255),	# Column name
    shortLabel varchar(255),	# Short label
    longLabel varchar(255),	# Long label
    valField varchar(255),	# Val field name
    clinicalTable varchar(255),	# Table of clinical data
    priority float,	# Priority
    filterType varchar(255),	# Filter Type - minMax or coded
    visibility varchar(255),	# Visibility
    groupName varchar(255)	# Group Name
) engine 'MyISAM';

CREATE TABLE raDb (
    name varchar(255),	# Table name for genomic data
    downSampleTable varchar(255),	# Down-sampled table
    sampleTable varchar(255),	# Sample table
    clinicalTable varchar(255),	# Clinical table
    columnTable varchar(255),	# Column table
    shortLabel varchar(255),	# Short label
    longLabel varchar(255),	# Long label
    expCount int unsigned,	# Number of samples
    groupName varchar(255),	# Group name
    microscope varchar(255),	# hgMicroscope on/off flag
    aliasTable varchar(255),	# Probe to gene mapping
    dataType varchar(255),	# data type (bed 15)
    platform varchar(255),	# Expression, SNP, etc.
    security varchar(255),	# Security setting (public, private)
    profile varchar(255),	# Database profile
    gain float,	# Gain
    priority float,	# Priority for sorting
    url varchar(255),	# Pubmed URL
    wrangler varchar(255),	# Wrangler
    citation varchar(255),	# Citation
    article_title longblob,	# Title of publication
    author_list longblob,	# Author list
    wrangling_procedure longblob,	# Wrangling
              #Indices
    PRIMARY KEY(name)
);
""")
        while cls.c.nextset() is not None: pass

        cmd = '../scripts/genHeatmapSQL.py data_enum_order_quote2; cat out/* | mysql --defaults-file=%s hg18;' % cls.sandbox.defaults
        f = open('test.log', 'a')
        p = subprocess.Popen(cmd, shell=True, stdout=f, stderr=f)
        p.communicate()
        f.close()
        if p.returncode != 0:
            raise subprocess.CalledProcessError(p.returncode, cmd)

    @classmethod
    def tearDownClass(cls):
        cls.sandbox.shutdown()

    def test_clinical(self):
        """Test enum order in the clinical table"""
        self.c.execute("""select sampleName, color from clinical_test order by color,sampleName""")
        rows = self.c.fetchall()
        self.assertEqual(len(rows), 6)          # six samples
        self.assertEqual(rows[0][0], 'sample4') # sample name is sample4
        self.assertEqual(rows[0][1], 'Red')
        self.assertEqual(rows[1][0], 'sample1')
        self.assertEqual(rows[1][1], 'Red,Yellow')
        self.assertEqual(rows[2][0], 'sample3')
        self.assertEqual(rows[2][1], 'Blue,Yellow')
        self.assertEqual(rows[3][0], 'sample2')
        self.assertEqual(rows[3][1], 'Blue')
        self.assertEqual(rows[4][0], 'sample6')
        self.assertEqual(rows[4][1], 'Blue')
        self.assertEqual(rows[5][0], 'sample5')
        self.assertEqual(rows[5][1], 'Red,Blue')

def main():
    sys.argv = sys.argv[:1]
    unittest.main()

if __name__ == '__main__':
    main()
