<template>
    <div class="codemirror">
        <codemirror
          v-model="code" 
          :options="cmOption"
          @cursorActivity="onCmCursorActivity"
          @ready="onCmReady"
          @focus="onCmFocus"
          @blur="onCmBlur"
        />
        
      </div>
</template>
<script>

import { codemirror } from 'vue-codemirror'

// base style
import 'codemirror/lib/codemirror.css'

// theme css
import 'codemirror/theme/rubyblue.css'

// language
import 'codemirror/mode/sql/sql.js'
import 'codemirror/mode/vue/vue.js'

// active-line.js
import 'codemirror/addon/selection/active-line.js'

// styleSelectedText
import 'codemirror/addon/selection/mark-selection.js'
import 'codemirror/addon/search/searchcursor.js'

// highlightSelectionMatches
import 'codemirror/addon/scroll/annotatescrollbar.js'
import 'codemirror/addon/search/matchesonscrollbar.js'
import 'codemirror/addon/search/searchcursor.js'
import 'codemirror/addon/search/match-highlighter.js'

// keyMap
import 'codemirror/mode/clike/clike.js'
import 'codemirror/addon/edit/matchbrackets.js'
import 'codemirror/addon/comment/comment.js'
import 'codemirror/addon/dialog/dialog.js'
import 'codemirror/addon/dialog/dialog.css'
import 'codemirror/addon/search/searchcursor.js'
import 'codemirror/addon/search/search.js'
import 'codemirror/keymap/sublime.js'

// foldGutter
import 'codemirror/addon/fold/foldgutter.css'
import 'codemirror/addon/fold/brace-fold.js'
import 'codemirror/addon/fold/comment-fold.js'
import 'codemirror/addon/fold/foldcode.js'
import 'codemirror/addon/fold/foldgutter.js'
import 'codemirror/addon/fold/indent-fold.js'
import 'codemirror/addon/fold/markdown-fold.js'
import 'codemirror/addon/fold/xml-fold.js'


export default {
    name: 'CodeEditor',
    
    components:{
      codemirror
    },
    props:{
      queryPlan: String

    },
    data(){
        return {
            code: this.queryPlan,
            cmOption: {
            tabSize: 4,
            foldGutter: true,
            styleActiveLine: true,
            lineNumbers: true,
            line: true,
            keyMap: "sublime",
            mode: 'text/x-sql',
            theme: 'ruby',
            extraKeys: {
              'F11'(cm) {
                cm.setOption("fullScreen", !cm.getOption("fullScreen"))
              },
              'Esc'(cm) {
                if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false)
            }
          }
        }
        }
    },
    methods:{
        onCmCursorActivity(codemirror) {
            console.debug('onCmCursorActivity', codemirror)
        },
        onCmReady(codemirror) {
            console.debug('onCmReady', codemirror)
        },
        onCmFocus(codemirror) {
            console.debug('onCmFocus', codemirror)
        },
        onCmBlur(codemirror) {
            console.debug('onCmBlur', codemirror)
        }
    },
    watch: {
      queryPlan() {
      // Trigger any necessary actions when the computedValue prop changes
      // For example, you can call a method or update local component data
        
        this.code = this.queryPlan;
      },
  }
}
</script>

<style lang="scss" scoped>
  .example {
    display: flex;
    height: 100%;

    .codemirror{
      width: 50%;
      height: 100%;
      margin: 0;
      font-family: monospace;
      overflow: auto;
    }

  }
</style>