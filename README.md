pyKeynoteTweet.py by [Heiko Behrens][1] allows you to send out tweets while you give your presentation with Keynote. It does so by looking for the pattern

    [twitter]your tweet[/twitter]

in your presenter's notes. Each time a new slide with this pattern appears during presentation mode it sends out the payload using twurl.

Setup
=====

 1. Download and install [twurl][2] according to it's fabulous documentation.

 2. Download and install [appscript][3] Python module.

 3. Prepare your presentation.

 4. Run pyKeynoteTweet.py and rock your audience!

Notes
=====
Please note that this script relies on the default account of [twurl][2]. You can use this fact to test your tweets and/or tweet with different accounts. Also, [open an issue][4] if you missing a feature such as adding hash tags automatically.

  [1]: http://HeikoBehrens.net
  [2]: https://github.com/marcel/twurl
  [3]: http://appscript.sourceforge.net
  [4]: https://github.com/HBehrens/pyKeynoteTweet/issues