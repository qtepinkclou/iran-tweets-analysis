"""Constant variables and class for manipulating data in iran tweets analysis project."""

from collections import defaultdict
import re


CLEAR_LIST = [
    'i', 'me', 'my', 'amp', 'th',
    'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
    "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
    'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
    'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and',
    'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
    'about', 'against',
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
    'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
    'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
    "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain',
    'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',
    "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't",
    'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn',
    "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
]

DATE_PATTERN = re.compile(r'[0-1][0-9]-[0-3][0-9]')
WORD_PATTERN = re.compile(r"([a-zA-Z_]+)")
LINK_PATTERN = re.compile(r'https:\/\/t\.co\/[0-9a-zA-z]{10}')
LATIN_HASHTAG = re.compile(r'\#([a-zA-Z0-9_]+)')
PERSIAN_HASHTAG = re.compile(r'\#([\u0600-\u065F\u066E-\u06D5\_]+)')
PERSIAN_WORD = re.compile(r'([\u0600-\u065F\u066E-\u06D5]+)')
USER_PATTERN = re.compile(r'\@([a-zA-Z0-9_]+)')


class Wrangler:
    """For use in manipulating data in iran tweets analysis project."""

    def __init__(self) -> None:
        """init method"""
        self.words_dict = defaultdict(int)
        self.del_words_dict = defaultdict(int)
        self.latin_hashtags = defaultdict(int)
        self.persian_hashtags = defaultdict(int)
        self.persian_words = defaultdict(int)
        self.tweet_texts_list = []
        self.tweet_hashtags_list = []

    def tweet_to_text(self, tweets_list: list):
        """take only words in a tweet and group them as lists."""
        for tweet in tweets_list:
            interim = LINK_PATTERN.sub('', tweet.lower())
            interim = LATIN_HASHTAG.sub('', interim)
            words = WORD_PATTERN.findall(interim)
            self.tweet_texts_list.append(words)

    def tweet_to_hashtag(self, tweets_list: list):
        """take only hashtags in a tweet and group them as lists."""
        for tweet in tweets_list:
            interim = LINK_PATTERN.sub('', tweet.lower())
            hashtags = LATIN_HASHTAG.findall(interim)
            self.tweet_hashtags_list.append(hashtags)

    def disect_text(self, tweets_list: list):
        '''Disect the given tweets-list consisting of
        text by its persian and latin hashtags and words,
        as well as removing links.'''
        for tweet_text in tweets_list:
            if isinstance(tweet_text, str):
                tweet_text = tweet_text.lower()
                sentences = LINK_PATTERN.sub('', tweet_text)

                lat_hash = LATIN_HASHTAG.findall(sentences)
                for has in lat_hash:
                    self.latin_hashtags[has] += 1
                sentences = LATIN_HASHTAG.sub('', sentences)

                pers_hash = PERSIAN_HASHTAG.findall(sentences)
                for has in pers_hash:
                    self.persian_hashtags[has] += 1
                sentences = PERSIAN_HASHTAG.sub('', sentences)

                pers_word = PERSIAN_WORD.findall(sentences)
                for wrd in pers_word:
                    self.persian_words[wrd] += 1
                sentences = PERSIAN_WORD.sub('', sentences)
                sentences = sentences.strip()

                words = WORD_PATTERN.findall(sentences)
                for wrd in words:
                    self.words_dict[wrd] += 1

                self.clear_dict(CLEAR_LIST)

    def clear_dict(self, key_list: list, dict_name='latin_words'):
        '''Pop the list of words to be eliminated from
           the dictionary of words and put into the
           deleted '''
        dicti = self.choose_dict(dict_name)
        for key in key_list:
            if key in dicti.keys():
                value = dicti.pop(key)
                self.del_words_dict[key] = value

    def sort_to_list(self, dict_name='latin_words', num=25):
        """Sort the given group of words or hashtags by
            their occurence count, save to a list and print
            the first 'num' elements."""
        dicti = self.choose_dict(dict_name)
        sorted_list = sorted(
           dicti.items(),
            key=lambda x:x[1],
            reverse=True
        )
        print('New len of list is : ' + str(len(sorted_list)))
        print('First ' + str(num) + ' elements in list are: \n')
        for i in range(num):
            print(sorted_list[i])
        return sorted_list

    def choose_dict(self, dict_name):
        """return dict given by key word."""
        if dict_name == 'latin_words':
            return self.words_dict
        elif dict_name == 'persian_words':
            return self.persian_words
        elif dict_name == 'persian_hashtags':
            return self.persian_hashtags
        elif dict_name == 'latin_hashtags':
            return self.latin_hashtags
        else:
            raise NoDictError('Dict type does not exist')

    def date_occ_group(self, dates_list:list, group_len: list):
        """Count average tweet counts by day given dates_list
           and group_len which gives the list of day groups
           to look for."""
        def chunks(iterable, value: int):
            """Yield successive chunks with size value from iterable."""
            for i in range(0, len(iterable)):
                yield list(iterable[i:i + value])

        days_dict = dict()
        for day_group in group_len:
            days_list = []
            for group in chunks(dates_list, day_group):
                tot = 0
                for date_duo in group:
                    (_, count) = date_duo
                    tot += count
                days_list.append(
                    (
                       'between ' \
                       + group[0][0].strftime('%m-%d') \
                       + ' - ' \
                       + group[-1][0].strftime('%m-%d'),
                        tot/day_group
                    )
                )
            days_dict[day_group] = days_list
        return days_dict

    def compare_freq(
        self,
        group_word_list: list,
        dataset_word_list: list,
        len_group: int,
        len_dataset: int,
        num=100
        ):
        """Given two lists containing sets of
           (word, frequency) compare and record
           rise in ratio of frequency and return
           in a list of sets along with original
           information."""

        match_words_group = group_word_list[0:num]
        match_words_overall = []
        for row in match_words_group:
            for elem in dataset_word_list:
                if row[0] == elem[0]:
                    match_words_overall.append(elem)

        group_word_freq = []
        dataset_word_freq = []
        for row in group_word_list:
            freq = row[1]/len_group
            group_word_freq.append((row[0], freq))
        for row in dataset_word_list:
            freq = row[1]/len_dataset
            dataset_word_freq.append((row[0], freq))

        word_freq_comparison = []
        for row_g in group_word_freq:
            for row_d in dataset_word_freq:
                if row_g[0] == row_d[0]:
                    word_freq_comparison.append(
                        (row_g[0], (row_g[1]-row_d[1])/row_d[1], row_g[1], row_d[1])
                    )

        s_word_freq_comparison = sorted(
            word_freq_comparison,
            key=lambda x:x[2],
            reverse=True
        )
        return s_word_freq_comparison


class NoDictError(Exception):
    """no dictionary by that name."""
