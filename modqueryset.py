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
import random
from django.db.models.query import QuerySet

class QuerySetError(TypeError): pass
class NumToSelectError(TypeError): pass

def rand_subset(queryset, num_to_select):
  if type(queryset) is not QuerySet:
    raise QuerySetError("<queryset> must be a django.db.models.query.QuerySet")
  if type(num_to_select) is not int:
    raise NumToSelectError("<num_to_select> must be an integer.\n Got a (%s :%s) instead.\n" % (num_to_select, type(num_to_select)))
  num_to_select = max(num_to_select, 0)
  def rand_index(max_val): return int(random.random() * max_val)

  def rand_sample():
    everything = list(queryset.values_list("pk", flat=True))
    return [everything.pop(rand_index(len(everything))) for i in range(num_to_select)]
  def rand_sample_complement():
    everything = list(queryset.values_list("pk", flat=True))
    for i in range(queryset.count() - num_to_select):
      everything.pop(rand_index(len(everything)))
    return everything

  def results(): return rand_sample() if num_to_select < (queryset.count() / 2) else rand_sample_complement()
  def model_type(): return type(queryset[0])
  return model_type().objects.filter(pk__in=results()) if queryset.count() else queryset.none()
