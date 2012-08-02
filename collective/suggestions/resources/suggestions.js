var suggestions = {};

suggestions.init = function(){
	jq('#suggestion-button').hover(function(){
		jq(this).find('img').toggle();
	})
}

jq(document).ready(suggestions.init);