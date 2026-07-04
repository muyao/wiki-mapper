def is_bad_url(url):
	if "://en.wikipedia.org/" not in url:
		return True
	if "/wiki/" not in url:
		return True
	if "/wiki/Category:" in url:
		return True
	if "/wiki/File:" in url:
		return True
	if "/wiki/Help:" in url:
		return True
	if "/wiki/Portal:" in url:
		return True
	if "/wiki/Special:" in url:
		return True
	if "/wiki/Template:" in url:
		return True
	if "/wiki/Template_talk:" in url:
		return True
	if "/wiki/Talk:" in url:
		return True
	if "/wiki/Wikipedia:" in url:
		return True
	if "/wiki/Main_Page" in url:
		return True
	if "/wiki/Lists_of_" in url:
		return True
	if "/wiki/List_of_" in url:
		return True
	if "(disambiguation)" in url:
		return True
	return False

def add_to_output(url, output_dict, val):
	if url not in output_dict:
		output_dict[url] = val
		return
	p = output_dict[url]
	for v in val:
		if v in p:
			continue
		p.append(v)