def getFullGroupData(group):
    students = group.students.all()
    exercises = group.exercises.all()
    scores = []
    for exercise in exercises:
        scores.append(exercise.scores.all())
    return [students, exercises, scores]
