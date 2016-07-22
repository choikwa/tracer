
import sys

filename = sys.argv[1]

def marker(annot, depth, bnum):
  return 'errs() << __func__ << "-' + \
    annot + str(depth) + '-' + str(bnum) + '\\n";'

def ifFirstWordIsIn(ss, listOfWords):
  if len(ss.split()) == 0: return False
  return ss.split()[0] in listOfWords

newf = ''
with open(filename) as f_in:
  depth = 0
  bnum = 0
  multiline_comment = False
  for chunk in f_in:
    ignoreLine = False
    for i,ch in enumerate(chunk):
      newf+=ch
      if multiline_comment:
        if ch == '*' and chunk[i+1] == '/':
          multiline_comment = False
      elif not ignoreLine:
        if ch == '{':
          depth+=1
          bnum+=1
          newf+=marker('entr', depth, bnum) 
        elif ch == '}':
          if not ifFirstWordIsIn(chunk[i+1:], ['else', 'catch']):
            newf= newf[:-1] + marker('exit', depth, bnum) + '}'
          depth-=1
        elif ch == '/':
          nchar = chunk[i+1]
          if nchar == '/':
            ignoreLine = True;
          elif nchar == '*':
            multiline_comment = True
        

with open('trace.out', 'w') as f_out:
  f_out.write(newf)
