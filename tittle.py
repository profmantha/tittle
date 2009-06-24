#########################################################################
#
#  Tittle is a frontend to Remember the Milk
#
#  Copyright (C) 2009 Jordan Mantha <jordan.mantha@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##########################################################################

from python_rtm.rtm import *

config_file="/home/mantha/.tittle"

inconfig = open(config_file, "r")
config = inconfig.readlines()
api_key = config[0].rstrip("\n")
shared_secret = config[1].rstrip("\n")
token = config[2].rstrip("\n")

rtmc = RTMClient(api_key, shared_secret, token)
task_data = rtmc.tasks.rtm.tasks.getList()
list_data = rtmc.tasks.rtm.lists.getList()

list_dict = {}
for i in list_data.lists.list:
	list_dict[i.name] =  i.id

k=1

for list in list_dict:
	#print "%i: %s" % (k,list)
	print list
	for i in xrange(len(task_data.tasks.list)):
		if task_data.tasks.list[i].id == list_dict[list] and hasattr(task_data.tasks.list[i], "taskseries"):
			for j in xrange(len(task_data.tasks.list[i].taskseries)):
				if not task_data.tasks.list[i].taskseries[j].task.completed:
					print ("   %i: %s" %(k,task_data.tasks.list[i].taskseries[j].name))
				else:
					print ("   %i: %s (done)" %(k,task_data.tasks.list[i].taskseries[j].name))
				k += 1
			k = 1

