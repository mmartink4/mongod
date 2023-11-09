def popularHashtags(tweets):
    select = tweets.find({
        "entities.hashtags.text": { "$exists": True }
	})
    hash_count = {}
    for tweet in select:
        for hashtag in tweet['entities']['hashtags']:
            if hashtag['text'] in hash_count:
                hash_count[hashtag['text']] += 1
            else:
                hash_count[hashtag['text']] = 1
    hash_count = sorted(hash_count.items(), key=lambda x: x[1], reverse=True)
    return hash_count

def popularUrls(tweets):
    select = tweets.find({
        "entities.urls.expanded_url": { "$exists": True }
	})
    urls_count = {}
    for tweet in select:
        for url in tweet['entities']['urls']:
            if url['expanded_url'] in urls_count:
                urls_count[url['expanded_url']] += 1
            else:
                urls_count[url['expanded_url']] = 1
    urls_count = sorted(urls_count.items(), key=lambda x: x[1], reverse=True)
    return urls_count

def popularMentions(tweets):
    select = tweets.find({
        "entities.user_mentions.screen_name": { "$exists": True }
	})
    user_count = {}
    for tweet in select:
        for mention in tweet['entities']['user_mentions']:
            if mention['screen_name'] in user_count:
                user_count[mention['screen_name']] += 1
            else:
                user_count[mention['screen_name']] = 1
    user_count = sorted(user_count.items(), key=lambda x: x[1], reverse=True)
    return user_count

def popularLangs(tweets):
    select = tweets.find({
        "lang": { "$exists": True }
	})
    lang_count = {}
    for tweet in select:
        if tweet['lang'] in lang_count:
            lang_count[tweet['lang']] += 1
        else:
            lang_count[tweet['lang']] = 1
    lang_count = sorted(lang_count.items(), key=lambda x: x[1], reverse=True)
    return lang_count

def popularCities(tweets):
	select = tweets.find({
		"place.full_name": { "$exists": True }
	})
	city_count = {}
	for tweet in select:
		if tweet['place']['full_name'] in city_count:
			city_count[tweet['place']['full_name']] += 1
		else:
			city_count[tweet['place']['full_name']] = 1
	city_count = sorted(city_count.items(), key=lambda x: x[1], reverse=True)
	return city_count

def popularCountries(tweets):
	select = tweets.find({
		"place.country": { "$exists": True }
	})
	country_count = {}
	for tweet in select:
		if tweet['place']['country'] in country_count:
			country_count[tweet['place']['country']] += 1
		else:
			country_count[tweet['place']['country']] = 1
	country_count = sorted(country_count.items(), key=lambda x: x[1], reverse=True)
	return country_count

def popularWords(tweets):
    select = tweets.find({
		"text": { "$exists": True }
	})
    word_count = {}
    for tweet in select:
        for word in tweet['text'].split():
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return word_count

def popularAccounts(tweets):
    select = tweets.find({
        "user.screen_name": { "$exists": True }
    })
    user_count = {}
    for tweet in select:
        # RTs
        if tweet['user']['screen_name'] in user_count:
            user_count[tweet['user']['screen_name']] += tweet['retweet_count']
        else:
            user_count[tweet['user']['screen_name']] = 1
        # Replies
        if tweet['in_reply_to_screen_name'] in user_count:
            user_count[tweet['in_reply_to_screen_name']] += 1
        else:
            user_count[tweet['in_reply_to_screen_name']] = 1
        # Mentions
        for mention in tweet['entities']['user_mentions']:
            if mention['screen_name'] in user_count:
                user_count[mention['screen_name']] += 1
            else:
                user_count[mention['screen_name']] = 1
    user_count = sorted(user_count.items(), key=lambda x: x[1], reverse=True)
    user_count.pop(0) # remove None
    return user_count

def getAllUsers(tweets):
    select = tweets.find({
        "user.screen_name": { "$exists": True }
    })
    users = {}
    for tweet in select:
        if tweet['user']['screen_name'] not in users:
            users[tweet['user']['screen_name']] = {
                'id': tweet['user']['id'],
                'username': tweet['user']['screen_name'],
                'name': tweet['user']['name'],
                'description': tweet['user']['description'],
                'followers': tweet['user']['followers_count']
            }
    return users

def getUser(tweets, username):
    select = tweets.find({
        "user.screen_name": { "$exists": True }
    })
    retweets = tweets.find({
        "retweeted_status.user.screen_name": { "$exists": True }
    })
    for tweet in select:
        if tweet['user']['screen_name'] == username:
            return tweet['user']
    for tweet in retweets:
        if tweet['retweeted_status']['user']['screen_name'] == username:
            return tweet['retweeted_status']['user']
    return None
