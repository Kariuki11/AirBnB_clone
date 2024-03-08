#!/usr/bin/python3
"""Defines the HBnB console."""

import cmd
import re
import json
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
  """Parse conflicts with curly braces and square brackets for elastic attribute updates."""
  curly_braces = re.search(r"\{(.*?)\}", arg)
  brackets = re.search(r"\[(.*?)\]", arg)
  if curly_braces is None:
    if brackets is None:
      return [i.strip(",") for i in shlex.split(arg)]
    else:
      lexer = shlex.split(arg[:brackets.span()[0]])
      retl = [i.strip(",") for i in lexer]
      retl.append(brackets.group())
      return retl
  else:
    lexer = shlex.split(arg[:curly_braces.span()[0]])
    retl = [i.strip(",") for i in lexer]
    retl.append(curly_braces.group())
    return retl


class HBNBCommand(cmd.Cmd):
  """Defines the HolbertonBnB command interpreter.

  Attributes:
      prompt (str): The command prompt.
      __classes (list): List of supported class names for validation.
  """

  prompt = "(hbnb) "
  __classes = {
      "BaseModel",
      "User",
      "State",
      "City",
      "Place",
      "Amenity",
      "Review"
  }

  def emptyline(self):
    """Do nothing after receiving a void line."""
    pass

  def default(self, arg):
    """Default behavior for cmd module when input is invalid"""
    argdict = {
        "all": self.do_all,
        "show": self.do_show,
        "destroy": self.do_destroy,
        "count": self.do_count,
        "update": self.do_update
    }
    match = re.search(r"\.", arg)
    if match is not None:
      argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
      match = re.search(r"\((.*?)\)", argl[1])
      if match is not None:
        command = [argl[1][:match.span()[0]], match.group()[1:-1]]
        if command[0] in argdict.keys():
          call = "{} {}".format(argl[0], command[1])
          return argdict[command[0]](call)
    print("* Unknown syntax: {}".format(arg))
    return False

  def do_quit(self, arg):
    """Quit command to exit the program."""
    return True

  def do_EOF(self, arg):
    """EOF signal to exit the program."""
    print("")
    return True

  def do_create(self, arg):
    """Usage: create <class>
    Makes a new class instance and print its id.
    """
    argl = parse(arg)
    if len(argl) == 0:
      print("* class name missing *")
    elif argl[0] not in HBNBCommand.__classes:
      print("* class doesn't exist *")
    else:
      print(eval(argl[0])().id)
      storage.save()

  def do_show(self, arg):
    """Usage: show <class> <id> or <class>.show(<id>)
    Shows the string representation of class instance of a given id.
    """
    argl = parse(arg)
    objdict = storage.all()
    if len(argl) == 0:
      print("* class name missing *")
    elif argl[0] not in HBNBCommand.__classes:
      print("* class doesn't exist *")
    elif len(argl) == 1:
      print("* instance id missing *")
    elif "{}.{}".format(argl[0], argl[1]) not in objdict:
      print("* no instance found *")
    elif len(argl) == 1:
        print("* instance id missing *")
    elif "{}.{}".format(argl[0], argl[1]) not in objdict:
        print("* no instance found *")
    else:
        print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
      """Usage: destroy <class> <id> or <class>.destroy(<id>)
      Delete a class instance of a given id."""
      argl = parse(arg)
      objdict = storage.all()
      if len(argl) == 0:
        print("* class name missing *")
      elif argl[0] not in HBNBCommand.__classes:
        print("* class doesn't exist *")
      elif len(argl) == 1:
        print("* instance id missing *")
      elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
        print("* no instance found *")
      else:
        del objdict["{}.{}".format(argl[0], argl[1])]
        storage.save()

    def do_all(self, arg):
      """Usage: all or all <class> or <class>.all()
      Display string representations of all instances of a given class.
      Assuming that no class is determined it displays all instantiated objects."""
      argl = parse(arg)
      if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
        print("* class doesn't exist *")
      else:
        objl = []
        for obj in storage.all().values():
          if len(argl) > 0 and argl[0] == obj._class.name_:
            objl.append(obj.str())
          elif len(argl) == 0:
            objl.append(obj.str())
        print(objl)

    def do_count(self, arg):
      """Usage: count <class> or <class>.count()
      Recover the quantiy of occurence of a given class."""
      argl = parse(arg)
      count = 0
      for obj in storage.all().values():
        if argl[0] == obj._class.name_:
          count += 1
      print(count)

    def do_update(self, arg):
      """Usage: update <class> <id> <attribute_name> <attribute_value> or
      <class>.update(<id>, <attribute_name>, <attribute_value>) or
      <class>.update(<id>, <dictionary>)
      Update a class occurence of a given id by adding or refreshing
      a given attribute key/value pair or dictionary."""
      argl = parse(arg)
      objdict = storage.all()

      if len(argl) == 0:
        print("* class name missing *")
        return False
      if argl[0] not in HBNBCommand.__classes:
        print("* class doesn't exist *")
        return False
      if len(argl) == 1:
        print("* instance id missing *")
        return False
      if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
        print("* no instance found *")
        return False
      if len(argl) == 2:
        print("* attribute name missing *")
        return False
      if len(argl) == 3:
        try:
          type(eval(argl[2])) != dict
        except NameError:
          print("* value missing *")
          return False
     

      if len(argl) == 4:
        obj = objdict["{}.{}".format(argl[0], argl[1])]
        if argl[2] in obj.dict.keys():
          valtype = type(obj.dict[argl[2]])
          obj.dict[argl[2]] = valtype(argl[3])
        else:
          obj.dict[argl[2]] = argl[3]
      elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
              if k in obj.dict.keys() and type(obj.dict[k]) in {str, int, float}:
                valtype = type(obj.dict[k])
                obj.dict[k] = valtype(v)
              else:
                obj.dict[k] = v
      storage.save()
      
          # if _name_ == '_main_':
            # HBNBCommand().cmdloop()