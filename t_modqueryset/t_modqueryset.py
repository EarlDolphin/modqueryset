#!/usr/bin/env python3
#Copyright (c) 2015, EarlDolphin
#All rights reserved.
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#* Redistributions of source code must retain the above copyright notice, this
#list of conditions and the following disclaimer.
#* Redistributions in binary form must reproduce the above copyright notice,
#this list of conditions and the following disclaimer in the documentation
#and/or other materials provided with the distribution.
#* Neither the name of modasserts nor the names of its
#contributors may be used to endorse or promote products derived from
#this software without specific prior written permission.
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "t_modqueryset.settings")
import django
django.setup()

from django.db.models.query import QuerySet

import unittest
import random

from modasserts import myAsserts
from modqueryset import rand_subset, QuerySetError, NumToSelectError
from foo.models import Foo

class TestRandSubset(unittest.TestCase, myAsserts):
  def setUp(self):
    self.queryset = Foo.objects.filter(pk__lte=100)
    self.not_a_queryset = []
    self.good_nums_to_select = [
      int(min(0.5 * self.queryset.count(), max(0.01 * self.queryset.count(), 10))),
      0,
      -5,
      2 * self.queryset.count()
    ]
    self.bad_nums_to_select = [
      5.3,
      'foo',
      sum
    ]

  def test_setup(self):
    self.assertTrue(self.queryset.count() == 100)
    self.assertTrue(self.good_nums_to_select[0] in range(1, self.queryset.count() + 1))

  def test_args(self):
    for n in self.good_nums_to_select:
      rand_subset(queryset=self.queryset, num_to_select=n)
      self.assertFail(asrt=rand_subset, queryset=self.not_a_queryset, num_to_select=n)
      self.assertRaises(excClass=QuerySetError, callableObj=rand_subset, queryset=self.not_a_queryset, num_to_select=n)
      self.assertFail(asrt=self.assertRaises, excClass=Exception, callableObj=rand_subset, queryset=self.queryset, num_to_select=n)
    for n in self.bad_nums_to_select:
      self.assertFail(asrt=rand_subset, queryset=self.queryset, num_to_select=n)
      self.assertFail(asrt=rand_subset, queryset=self.not_a_queryset, num_to_select=n)
      self.assertRaises(excClass=NumToSelectError, callableObj=rand_subset, queryset=self.queryset, num_to_select=n)

  def test_return_type(self):
    r_ss = [rand_subset(queryset=self.queryset, num_to_select=n) for n in self.good_nums_to_select]
    exprs = [(type(r_s) is QuerySet) for r_s in r_ss]
    self.assertTrue(all(exprs))

  def test_return_size(self):
    def rs(k): return rand_subset(queryset=self.queryset, num_to_select=k)
    def expected_size(k): return max(0, min(k, self.queryset.count()))
    exprs = [(rs(n).count() == expected_size(n)) for n in self.good_nums_to_select]
    self.assertTrue(all(exprs))
  
  def test_no_duplicates(self):
    def expected_size(rs): return len(set(rs.values_list('pk', flat=True)))
    r_ss = [rand_subset(queryset=self.queryset, num_to_select=n) for n in self.good_nums_to_select]
    exprs = [(r_s.count() == expected_size(r_s)) for r_s in r_ss]
    self.assertTrue(all(exprs))

if __name__ == '__main__':
  unittest.main()
