## Guanqing Hao
## Homework 5

def readFromFile(filename):
    '''Read a file and store each non-empty line in a list'''
    fileList=[]
    f = open(filename, 'r')
    for line in f:
        line = line.strip()
        if line != '':
            fileList.append(line)
    f.close()
    return fileList

# ===== functions to read info from .txt =====
def readName(fileList):
    '''get name from the list'''
    name = fileList[0]
    return name

def isName(name):
    '''check if the first char is a capital letter'''
    ASCII = ord(name[0])
    if ASCII not in xrange(65, 91):
        raise RuntimeError, 'your name does not begin with a capital letter'

def isEmail(line):
    '''check if we can successfully get the email address.
    return boolean'''
    for char in line:
        if '@' == char:
            if (line[(len(line)-4):] == '.edu' or
                line[(len(line)-4):] == '.com'):
                length = len(line)
                for i in xrange(line.index('@'), length - 3):
                    ASCII = ord(line[i])
                    if ASCII in xrange(97, 123):
                        return True
    return False
                
def readEmail(fileList):
    '''return the email address as a string'''
    email = ''
    for line in fileList:
        if isEmail(line):
            email = line
    return email


def readCourses(fileList):
    '''return all courses as a string'''
    courses = ''
    for line in fileList:
        if line[:7] == 'Courses':
            for index in xrange(7, len(line)):
                if ord(line[index]) in xrange(65, 123):
                    courses = line[index:]
                    break
    return courses


def readProjects(fileList):
    '''return a list of projects
    first find the 'Projects' line and the ending line
    then return all lines in between'''
    beginIndex = 0
    endIndex = 0
    for line in fileList:
        if line == 'Projects':
            beginIndex = fileList.index(line)
        elif '----------' in line:
            endIndex = fileList.index(line)
    projects = fileList[beginIndex + 1 : endIndex]
    
    # if the word 'Projects' not found, return an empty list
    # similiarly, if ending line not found, the func should also return an empty list
    if beginIndex != 0:
        return projects
    else:
        return []

def readEducation(fileList):
    '''return a list with all education info'''
    education = []
    for line in fileList:
        judge1 = 'Bachelor' in line or 'Master' in line or 'Doctor' in line
        judge2 = 'University' in line
        if judge1 and judge2:
            education.append(line)
    return education

# ===== functions for HTML =====
def read_html(fileName):
    '''read from the initial html file and save contents in a list'''
    f = open(fileName, 'r')
    lines = f.readlines()
    del lines[-1]
    del lines[-1]
    f.close()
    return lines   

def surround_block(tag, text):
    '''add tags before and after some text to make an html block'''
    newText = '<' + tag + '>\n' + text + '\n</' + tag + '>\n'
    return newText

def basic_info(name, email):
    '''make an html block for basic info'''
    name = surround_block('h1', name)
    email = surround_block('p', email)
    return surround_block('div', name+email)

def education_info(education):
    '''make an html block for edu info'''
    title = surround_block('h2', 'Education')
    info = ''
    for ele in education:
        info += surround_block('li', ele)
    info = surround_block('ul', info)
    return surround_block('div', title+info)
    
def project_info(projects):
    '''make an html block for project info'''
    title = surround_block('h2', 'Projects')
    info = ''
    for project in projects:
        text = surround_block('p', project)
        info += surround_block('li', text)
    info = surround_block('ul', info)
    return surround_block('div', title+info)
    
def course_info(courses):
    '''make an html block for course info'''
    title = surround_block('h3', 'Courses')
    info = surround_block('span', courses)
    return surround_block('div', title+info)

def create_html(fileName, lines):
    '''create/rewrite a new html file with the given contents'''
    f = open(fileName, 'w')
    f.writelines(lines)
    f.close() 

# ===== main function =====
def main():
    fileName = 'resume.txt'
    fileList = readFromFile(fileName)

    # detect the contents in the resume
    name = readName(fileList)   #string
    isName(name) # raise RuntimeError if name not properly presented
    email = readEmail(fileList)   #string
    courses = readCourses(fileList)   #string
    projects = readProjects(fileList)   #list
    education = readEducation(fileList) #list

    # read html codes from the initial html file given in the homework
    html_file = 'resume_initial.html'
    
    # save the contents in a list and add contents
    html_list = read_html(html_file)
    html_list.append('<div id="page-wrap">\n')
    
    basicInfo = basic_info(name, email)
    html_list.append(basicInfo)
    
    eduInfo = education_info(education)
    html_list.append(eduInfo)
    
    projInfo = project_info(projects)
    html_list.append(projInfo)
    
    courseInfo = course_info(courses)
    html_list.append(courseInfo)

    html_list.append('''</div>\n</body>\n</html>''')
    
    # create a new html file and write the contents into the file
    create_html('resume.html', html_list)
    
    
if __name__ == '__main__':
    main()


    
