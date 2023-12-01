#include <vector>
#include <iterator>
#include <algorithm>
#include <utility>
#include <string>
#include <fstream>
#include <sstream>
#include <locale>
#include <regex>

#include <stdlib.h>
#include <string.h>

#include "tglang.h"
#include "fasttext/fasttext.h"

using namespace std;

string replace_text(string source_code, string first, string second, string pattern)
{
    stringstream restream;
    restream << first << "[^]*?" << second;
    auto rp_regex = regex(restream.str());
    stringstream stream;
    stream << regex_replace(source_code, rp_regex, pattern);
    source_code = stream.str();
    return source_code;
}

string remove_comments(string source_code)
{
    vector<pair<string, string>> signs =
    {
        pair<string, string>("\"\"\"", "\"\"\""),
        pair<string, string>("\\/\\*", "\\*\\/"),
        pair<string, string>("<!--", "-->"),
        pair<string, string>("--[", "]]"),
        pair<string, string>("\\/\\/", "(\n|$)"),
        pair<string, string>("# ", "(\n|$)"),
        pair<string, string>("--", "(\n|$)"),
        pair<string, string>(";;", "(\n|$)")
    };

    for(const auto& [first, second]: signs)
    {
        source_code = replace_text(source_code, first, second, " comment ");
    }

    return source_code;
}

string tokenize(string source_code)
{
    auto wp_regex = regex{"\\w+|[^\\w\\s]"};
    stringstream stream;
    vector<string> words(sregex_token_iterator(source_code.begin(), source_code.end(), wp_regex),
                         sregex_token_iterator());

    for(const auto& word: words)
    {
        stream << word << " ";
    }

    stream << endl;
    string clean_code = stream.str();
    return clean_code;
}

enum TglangLanguage tglang_detect_programming_language(const char *text)
{
    setlocale(LC_ALL, "");
    int max_length = 25000;

    fasttext::FastText textModel;
    textModel.loadModel("resources/text_model.ftz");

    fasttext::FastText codeModel;
    codeModel.loadModel("resources/code_model.ftz");

    ifstream languageFile("resources/languages.txt");
    vector<string> languages;
    string temp_language;

    while(languageFile >> temp_language)
    {
        languages.push_back(temp_language);
    }

    TglangLanguage language(TglangLanguage::TGLANG_LANGUAGE_OTHER);

    if(strlen(text) == 0)
    {
        return language;
    }

    string source_code(text, text + min((int)strlen(text), max_length));
    source_code = remove_comments(source_code);
    source_code = replace_text(source_code, "\"", "\"", " text ");
    string clean_code = tokenize(source_code);

    istringstream text_stream(clean_code);

    vector<pair<fasttext::real, string>> textPredictions;
    textModel.predictLine(text_stream, textPredictions, 1, 0.05);
    string text_code = textPredictions[0].second.substr(9, textPredictions[0].second.size() - 9);

    if(text_code == "OTHER")
    {
        return language;
    }

    istringstream code_stream(clean_code);

    vector<pair<fasttext::real, string>> codePredictions;
    codeModel.predictLine(code_stream, codePredictions, 1, 0.05);
    string language_code = codePredictions[0].second.substr(9, codePredictions[0].second.size() - 9);

    vector<string>::iterator it = find(languages.begin(), languages.end(), language_code);

    if(it != languages.end())
    {
        int index = it - languages.begin();
        language = static_cast<TglangLanguage>(index);
    }

    return language;
}
