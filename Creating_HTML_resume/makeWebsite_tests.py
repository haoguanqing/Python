from makeWebsite import *
import unittest

class TestMakeWebsite(unittest.TestCase):

# test the functions that read info from .txt   
    def test_readName(self):
        name = readName(['Gaga', 'What 123!@#'])
        self.assertEqual('Gaga', name, 'readName failed')

    def test_isName(self):
        self.assertRaises(RuntimeError, isName, '123')
        self.assertRaises(RuntimeError, isName, 'asd')

    def test_isEmail(self):
        line1 = 'asd@GAGA.com'
        line2 = 'asd@123.edu'
        line3 = 'asd@G1gA.org'
        line4 = '123ewaw===='
        line5 = '12sd@GaGA.com'
        self.assertFalse(isEmail(line1), ['isEmail failed'])
        self.assertFalse(isEmail(line2), ['isEmail failed'])
        self.assertFalse(isEmail(line3), ['isEmail failed'])
        self.assertFalse(isEmail(line4), ['isEmail failed'])
        self.assertTrue(isEmail(line5), ['isEmail failed'])

    def test_readEmail(self):
        fileList1 = ['asd@GAGA.com', 'asd@G1gA.org', 'asd@G1gA.org', '123ewaw====']
        fileList2 = ['AsD', '12sd@Ga1A.edu']
        self.assertEqual('', readEmail(fileList1), 'readEmail failed')
        self.assertEqual('12sd@Ga1A.edu', readEmail(fileList2), 'readEmail failed')

    def test_readCourses(self):
        fileList1 = ['asd', '123']
        fileList2 = ['asd', 'Courses:-@#@#123 course1, course2', '123qwe==']
        self.assertEqual('', readCourses(fileList1))
        self.assertEqual('course1, course2', readCourses(fileList2))

    def test_readProjects(self):
        fileList1 = ['asd', 'what', 'hahafwef?', '--------------']
        fileList2 = ['name', 'Projects', 'proj1', 'proj2']
        fileList3 = ['asd', 'Projects', 'proj1', 'proj2', '---------------', '123']
        self.assertEqual([], readProjects(fileList1))
        self.assertEqual([], readProjects(fileList2))
        self.assertEqual(['proj1', 'proj2'], readProjects(fileList3))

    def test_readEducation(self):
        fileList1 = ['Master', 'Bachelor', 'Doctor', 'University']
        fileList2 = ['Master University', 'Doctor gaga in University 2']
        self.assertEqual([], readEducation(fileList1))
        self.assertEqual(['Master University', 'Doctor gaga in University 2'], readEducation(fileList2))

# test the functions to create HTML =====
    def surround_block(self):
        text = surround_block('ga', 'gaga')
        self.assertEqual('''<ga>\ngaga\n</ga>\n''', text)

    def test_basic_info(self):
        name = 'gaga'
        email = 'ga@seas'
        self.assertEqual('''<div>
<h1>
gaga
</h1>
<p>
ga@seas
</p>

</div>
''', basic_info(name, email))

    def test_education_info(self):
        education = ['a', 'b']
        self.assertEqual('''<div>
<h2>
Education
</h2>
<ul>
<li>
a
</li>
<li>
b
</li>

</ul>

</div>
''', education_info(education))

    def test_project_info(self):
        proj = ['a', 'b']
        self.assertEqual('''<div>
<h2>
Projects
</h2>
<ul>
<li>
<p>
a
</p>

</li>
<li>
<p>
b
</p>

</li>

</ul>

</div>
''', project_info(proj))

    def test_course_info(self):
        courses = 'a,b,c'
        self.assertEqual('''<div>
<h3>
Courses
</h3>
<span>
a,b,c
</span>

</div>
''', course_info(courses))
        

unittest.main()














