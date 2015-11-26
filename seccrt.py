# $language = "Python"

# $interface = "1.0"

# a litter script which for capture the screen output and save to the file.

import time

#need config below:
rootdir = "/root/xxx"
filedir = "xxx/xxxx/"
prompt = ">"
localrootpath = "E:\work\\"





showlistcmd = "ls -l\n" 

def main():
  crt.Screen.Synchronous = True

  winfiledir = filedir.replace("/", "\\")

  localdirpath = localrootpath + winfiledir

  crt.Screen.Send("cd " + rootdir + "\n")
  crt.Screen.WaitForString("\n")

  crt.Screen.Send("cd " + filedir + "\n")
  crt.Screen.WaitForString("\n")

  crt.Screen.Send(showlistcmd)
  crt.Screen.WaitForString("\n")
  b = crt.Screen.ReadString(prompt)

  filelist = b.splitlines()
  newprompt = filedir[-3:-1] + ">"

  for line in filelist:

    if line[0] == "-" :
      fileinfo = line.split()
      filename = fileinfo[-1]
      localfile = localdirpath + filename
      newfile = open(localfile, 'w')
      
      catcmd = "cat " + filename + "\n"
      crt.Screen.Send(catcmd)
      crt.Screen.WaitForString("\n")
      ret = crt.Screen.ReadString(newprompt)
      ret1 = ret.splitlines()

      for l in range(len(ret1)) :
        if l != len(ret1) - 1 :
          newfile.write(ret1[l])
          if l != len(ret1) - 2 : 
            newfile.write("\n")

      newfile.close()

      time.sleep(1)

main()
