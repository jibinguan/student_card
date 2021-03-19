import pandas as pd
import json
import sys

#json_filename = 'Example1/submit.json'
#PATH = r'Example1/'

def init(argv):
    inputfiles = ''
    outputfile = ''
    file_num = len(sys.argv)
    for i in argv[1:]:
        inputfiles = argv[1:-1]
        outputfile = argv[-1]
    #print('input file:', inputfiles)
    #print('output file:', outputfile)

    mergeresult, courseAverage, totalAverage = init_and_joint_tables(inputfiles)
    generate_jason(mergeresult, courseAverage, totalAverage, outputfile)

def load_from_cvs(filename):
    try:
        data = pd.read_csv(filename, index_col=0)
        return data
    except:
        return "load files fail."


def init_and_joint_tables(inputfile):
    for file in inputfile:
        if file == 'students.csv':
            students = load_from_cvs("students.csv")
        elif file == 'courses.csv':
            courses = load_from_cvs("courses.csv")
        elif file == 'tests.csv':
            tests = load_from_cvs("tests.csv")
        elif file == 'marks.csv':
            marks = load_from_cvs("marks.csv")
        else:
            print("input files error")
            break
    # print(students,courses,tests,marks)
    marks_student = marks.join(students, on='student_id')
    marks_student_tests = marks_student.join(tests, on='test_id')
    result = marks_student_tests.join(courses, on='course_id', lsuffix='_student', rsuffix='_course')
    order = ['student_id', 'name_student', 'course_id', 'name_course', 'teacher', 'mark', 'weight']
    new = result[order]
    # print(new)

    courseAverage = result.groupby(['student_id', 'course_id']).apply(
        lambda x: (x['mark'] * x['weight'] / 100).sum().round(2))
    # print(courseAverage.to_dict())
    totalAverage = courseAverage.groupby('student_id').mean().round(2)
    # print(totalAverage.to_dict())
    return new, courseAverage, totalAverage


def generate_jason(mergeresult, courseAverage, totalAverage, outputfile):
    student_info = {}
    data = json.loads(json.dumps(student_info))
    df = mergeresult.loc[mergeresult['student_id'] == 1, :]
    df2 = mergeresult.loc[(mergeresult['student_id'] == 1) & (mergeresult['course_id'] == 1), :]
    courses = []
    students = []
    valid_weight = mergeresult.groupby(['student_id', 'course_id']).apply(lambda x: (x['weight'].sum())).tolist()
    for k, v in totalAverage.items():
        student = {'id': k, 'name': mergeresult.loc[mergeresult['student_id'] == k, :].iloc[0, 1], 'totalAverage': v,
                   'courses': {}}
        for j, m in courseAverage.items():
            (x, y) = j
            if x == k:
                df2 = mergeresult.loc[(mergeresult['student_id'] == x) & (mergeresult['course_id'] == y), :]
                course_name = df2.iloc[0, 3]
                teacher_name = df2.iloc[0, 4]
                student_id = df2.iloc[0, 0]
                course_id = df2.iloc[0, 2]
                if valid_weight[y - 1] == 100:
                    course = {'id': y, 'name': course_name, 'teacher': teacher_name, 'courseAverage': m}
                    courses.append(course)
                    student['courses'] = courses
                else:
                    course = {'id': y, 'name': course_name, 'teacher': teacher_name, 'courseAverage': m,
                              'error': 'Invalid course weights'}
                    courses.append(course)
                    student['courses'] = courses
                    continue
            else:
                courses = []
                continue
        students.append(student)
    data['students'] = students
    article = json.dumps(data, ensure_ascii=False)
    print(article)
    submit = outputfile
    with open(submit, 'w') as f:
        json.dump(article, f)

if __name__ == '__main__':
    init(sys.argv)

