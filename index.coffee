
command: "python3 myschedule/script.py"

render: (output) ->
  today = new Date()
  """
  <html><h1>TO DO LIST</br>(#{today.toLocaleString()})</h1>#{output}</html>
  """

# update: (output, domEl) ->
#   exec: (a, b) ->
#     cp = require('child_process')
#     cp.exec a b
#   exec "python3 /Users/william/Library/Application Support/Übersicht/widgets/myschedule/update.py -o output -d domEl", (err, stdout, stderr) -> output=stdout
#   today = new Date()
#   output = """
#   <html><h1>TO DO LIST</br>(#{today.toLocaleString()})</h1>#{output}</html>
#   """

style: """
  top: 30%
  right: 10px
  background: rgba(white, 0.7)
  background-size: 176px 84px
  border-radius: 0px
  border: 0px solid #fff
  box-sizing: border-box
  color: #141f33
  font-family: Helvetica Neue
  font-weight: 300
  line-height: 1.5
  margin-left: -170px
  padding: 20px 20px 20px
  width: 250px

  h1
    font-size: 20px
    font-weight: 300
    text-align: center

  em
    font-weight: 400
    font-style: normal

  li
    margin: 15px 0

  .running
    font-size: 18px
    color: red

  .comming
    font-size: 18px
    color: orange

  .rest
    font-size: 18px
    color: blue

  .quote
    font-size: 15px
    color: purple
    text-align: center
"""

refreshFrequency: 1000*600
