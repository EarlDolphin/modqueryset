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
from modqueryset import rand_subset
from foo.models import Foo

class TestRandSubset(unittest.TestCase, myAsserts):
  def setUp(self):
    self.queryset = Foo.objects.all()
    self.not_a_queryset = []
    self.num_to_select = int(min(0.5 * self.queryset.count(), max(0.01 * self.queryset.count(), 10)))
    self.negative_num_to_select = -5
    self.too_high_num_to_select = 2 * self.queryset.count()
    self.not_an_int = 5.3
    self.not_a_num = "foo"

  def test_arguments(self):
    good_args = {'queryset':self.queryset, 'num_to_select':self.num_to_select}
    raiseTypeError_args = {'excClass':TypeError, 'callableObj':rand_subset}

    argz = good_args.copy()
    argz.update(raiseTypeError_args)
    rand_subset(**good_args)
    self.assertFail(self.assertRaises, **argz)
    self.assertRaises(excClass=TypeError, callableObj=rand_subset, queryset=self.not_a_queryset, num_to_select=self.num_to_select)

  #def test_return_type(self):
    #self.assertTrue(type(rand_subset(queryset=self.queryset, num_to_select=self.num_to_select)) is QuerySet)
    #self.assertTrue(type(rand_subset(queryset=self.queryset, num_to_select=self.negative_num_to_select)) is QuerySet)
    #self.assertTrue(type(rand_subset(queryset=self.queryset, num_to_select=self.too_high_num_to_select)) is QuerySet)
  #def test_return_size(self):
    #self.assertTrue(rand_subset(queryset=self.queryset, num_to_select=self.num_to_select).count() == self.num_to_select)
    #self.assertTrue(rand_subset(queryset=self.queryset, num_to_select=self.negative_num_to_select).count() == 0)
    #self.assertTrue(rand_subset(queryset=self.queryset, num_to_select=self.too_high_num_to_select).count() == self.queryset.count())
  #def test_no_duplicates(self):
    #self.assertTrue(self.queryset.count() == len(set(self.queryset.values_list("pk", flat=True))))

  #def test_stressTest(self):


if __name__ == '__main__':
  unittest.main()
