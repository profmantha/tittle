# -*- coding: utf-8 -*-
### BEGIN LICENSE
# Copyright (C) 2009 Jordan Mantha <jordan.mantha@gmail.com>
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License version 3, as published 
#by the Free Software Foundation.
#
#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranties of 
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#PURPOSE.  See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along 
#with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from python_rtm.rtm import *

def RTMConfig():
    config_file="/home/mantha/.tittle"
    inconfig = open(config_file, "r")
    config = inconfig.readlines()
    api_key = config[0].rstrip("\n")
    shared_secret = config[1].rstrip("\n")
    token = config[2].rstrip("\n")
    return api_key, shared_secret, token

def RTMGetLists(api_key, shared_secret, token):

    rtmc = RTMClient(api_key, shared_secret, token)

    task_data = rtmc.tasks.rtm.tasks.getList()
    list_data = rtmc.tasks.rtm.lists.getList()

    list_dict = {}
    for i in list_data.lists.list:
        list_dict[i.name] =  i.id

    k=1

    list_text = []
    list_text_done = []
    for list in list_dict:
        #print "%i: %s" % (k,list)
        #print list
        for i in xrange(len(task_data.tasks.list)):
            if task_data.tasks.list[i].id == list_dict[list] and hasattr(task_data.tasks.list[i], "taskseries"):
                for j in xrange(len(task_data.tasks.list[i].taskseries)):
                    if not task_data.tasks.list[i].taskseries[j].task.completed:
                        list_text.append("[%s]:  %s" %(list,task_data.tasks.list[i].taskseries[j].name))
                    else:
                        list_text_done.append("[%s]:  %s" %(list,task_data.tasks.list[i].taskseries[j].name))
                    k += 1
                k = 1
    return list_text, list_text_done
