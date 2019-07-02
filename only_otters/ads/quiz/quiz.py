

class Quiz:
    """A quiz data object, containing simply the title & questions."""

    @classmethod
    def from_dict(cls, data):

        newobj = cls(data['title'])

        for q in data['questions']:
            newobj.add_question(**q)

        return newobj

    def __init__(self, title):
        self.title = title
        self.questions = []

    def add_question(self, name, desc, options, answer, multi=False):
        self.questions.append({
            'name': name,
            'desc': desc,
            'options': options,
            'multi': multi,
            'answer': answer
        })


def display_question(question):

    print(question['name'].upper(), '>')
    print('--' * 10)
    print(question['desc'])
    print('--' * 10)
    print('Options:', (', '.join(':'.join(map(str, o)) for o in enumerate(question['options']))))
    print('--' * 10)


# class QuizQuestion:

#     def __init__(self, question, owner):
#         self.owner = owner
#         for key, value in question.items():
#             setattr(self, key, value)

#     def send(self, answer):
#         self.owner.callback(answer)


class QuizTaker:
    """
    An object allowing to take a quiz. Keeps track of the score
    and serves the questions through an iterator.
    """
    def __init__(self, quiz):

        self.quiz = quiz

        self.idx = 0
        self.score = 0
        self.running = False
        self._answers = []

        self._question = None

    def take(self):
        """Return a quizz taker iterator. Iterate over it to get the
        questions."""
        quiz_taker_it = self._take()
        self.score = 0
        self.idx = 0
        # next(quiz_taker_it)
        return quiz_taker_it

    def _take(self):
        yield from self.quiz.questions

    def send(self, question, ans):
        """Send back the answer for the current question."""
        self._answers.append(ans)
        self.idx += 1
        self.score += ans == question['answer']

    @property
    def total_score(self):
        return '%s/%s' % (self.score, self.idx)


if __name__ == "__main__":

    quiz = Quiz('Bubbles')

    quiz.add_question(
        name='Roundness',
        desc='Are bubbles round ?',
        options=[
            'yes',
            'no'
        ],
        answer=0
    )

    quiz.add_question(
        name='Roundness',
        desc='Are bubbles sqiare ?',
        options=[
            'yes',
            'no'
        ],
        answer=0
    )

    quiz_taker = QuizTaker(quiz)

    # In a for loop
    for question in quiz_taker.take():
        display_question(question)
        ans = int(input())
        quiz_taker.send(question, ans)

    print('\033[91mTotal: %s\033[m' % quiz_taker.total_score)
    print()

    # Non-blocking
    quizTakerIterator = quiz_taker.take()
    while 1:

        # Fetch question
        try:
            question = next(quizTakerIterator)
        except StopIteration:
            break

        # Display question
        display_question(question)

        # Request answer
        a = int(input())

        # Feed answer to quiz taker
        quiz_taker.send(question, a)

    print('\033[91mTotal: %s\033[m' % quiz_taker.total_score)
    print()
