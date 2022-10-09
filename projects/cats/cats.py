"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    paragraphs_can_be_selected = [x for x in paragraphs if select(x)]
    if k >= len(paragraphs_can_be_selected):
        return ''
    else:
        return paragraphs_can_be_selected[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def if_topic_in(paragraph):
        clean_parahraph = remove_punctuation(paragraph)
        lower_paragraph = lower(clean_parahraph)
        words_of_paragraph = split(lower_paragraph)
        for t_word in topic:
            for p_word in words_of_paragraph:
                if t_word == p_word:
                    return True
        return False
    return if_topic_in
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    correct = 0
    index = 0
    while index < len(typed_words):
        if index >= len(reference_words):
            break
        else:
            if typed_words[index] == reference_words[index]:
                correct += 1
        index += 1
    if len(typed_words) == 0:
        return 0.0
    else:
        return correct / len(typed_words) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return (len(typed) * 60.0) / (elapsed * 5.0)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    for word in valid_words:
        if word == user_word:
            return user_word
    min_difference = 0x3f3f3f3f
    min_word = user_word
    for word in valid_words:
        difference = diff_function(user_word, word, limit)
        if difference < min_difference and difference <= limit:
            min_word = word
            min_difference = difference

    return min_word
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def shift_helper(str1, str2, cnt=0):
        if len(str1) == 0 or len(str2) == 0:
            return 0
        elif cnt > limit:
            return cnt
        else:
            if str1[0] == str2[0]:
                return shift_helper(str1[1:], str2[1:], cnt)
            else:
                return 1 + shift_helper(str1[1:], str2[1:], cnt + 1)
    characters_need_to_modify = shift_helper(start, goal)
    res = characters_need_to_modify + abs(len(start) - len(goal))
    return res
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    def diff_helper(str1, str2, cnt=0):
        if len(str2) == 0 or len(str1) == 0:
            # BEGIN
            "*** YOUR CODE HERE ***"
            if len(str2) == 0:
                return len(str1)
            else:
                return len(str2)
            # END
        elif cnt > limit:
            # BEGIN
            "*** YOUR CODE HERE ***"
            return cnt
            # END
        elif str1[0] == str2[0]:
            return diff_helper(str1[1:], str2[1:])
        else:
            add_diff = diff_helper(str1, str2[1:], cnt + 1)
            remove_diff = diff_helper(str1[1:], str2, cnt + 1)
            substitute_diff = diff_helper(str1[1:], str2[1:], cnt + 1)
            # BEGIN
            "*** YOUR CODE HERE ***"
            return min(add_diff, remove_diff, substitute_diff) + 1
            # END
    return diff_helper(start, goal)




def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""

    def diff_helper(str1, str2, cnt=0):
        if len(str2) == 0 or len(str1) == 0:
            # BEGIN
            "*** YOUR CODE HERE ***"
            if len(str2) == 0:
                return len(str1)
            else:
                return len(str2)
            # END
        elif cnt > limit:
            # BEGIN
            "*** YOUR CODE HERE ***"
            return cnt
            # END
        elif str1[0] == str2[0]:
            return diff_helper(str1[1:], str2[1:])
        else:
            add_diff = diff_helper(str1, str2[1:], cnt + 1)
            remove_diff = diff_helper(str1[1:], str2, cnt + 1)
            substitute_diff = diff_helper(str1[1:], str2[1:], cnt + 1)
            if len(str1) >= 2:
                swap_diff = diff_helper(str1[1] + str1[0] + str1[2:], str2, cnt + 1)
            # BEGIN
            "*** YOUR CODE HERE ***"
            return min(add_diff, remove_diff, substitute_diff, swap_diff) + 1
            # END

    return diff_helper(start, goal)


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    cnt = 0
    correct = 0
    while cnt < len(typed):
        if typed[cnt] == prompt[cnt]:
            correct += 1
        else:
            break
        cnt += 1
    progress = correct / len(prompt)
    send({'id': user_id, 'progress': progress})

    return progress
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    t = times_per_player
    number_of_timestamp = len(t[0])
    time = [[list[k + 1] - list[k] for k in range(number_of_timestamp - 1)] for list in t]
    return game(words, time)
   # return game(words, time)

    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    #create a balnk list of lists
    fastest = [[] for x in player_indices]

    for word_index in word_indices:
        current_word = word_at(game, word_index)
        fastest_player_index = 0
        fastest_time = time(game, fastest_player_index, word_index)
        for tmp in player_indices:
            if time(game, tmp, word_index) < fastest_time:
                fastest_player_index = tmp
                fastest_time = time(game, tmp, word_index)
        fastest[fastest_player_index] += [current_word]
    return fastest
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = True  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)