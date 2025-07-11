prompt_prettyHtml = function (diffs, is_undisplay_insert = false, is_undisplay_delete = false) {
  var html = [];
  var pattern_amp = /&/g;
  var pattern_lt = /</g;
  var pattern_gt = />/g;
  var pattern_para = /\n/g;
  for (var x = 0; x < diffs.length; x++) {
    var op = diffs[x][0];    // Operation (insert, delete, equal)
    var data = diffs[x][1];  // Text of change.
    var text = data.replace(pattern_amp, '&amp;').replace(pattern_lt, '&lt;')
      .replace(pattern_gt, '&gt;').replace(pattern_para, '&para;<br>');
    switch (op) {
      case DIFF_INSERT:
        if (is_undisplay_insert)
          break;
        html[x] = '<ins style="background:#c0fcc0;">' + text + '</ins>';
        break;
      case DIFF_DELETE:
        if (is_undisplay_delete)
          break;
        html[x] = '<span style="background:#fccaca;">' + text + '</span>';
        break;
      case DIFF_EQUAL:
        html[x] = '<span>' + text + '</span>';
        break;
    }
  }
  return html.join('');
};