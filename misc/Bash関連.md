# Bash関連

## シェルスクリプトで引数やオプション解析

### GNU getopt を使った従来の方法
 GNU getopt を使った場合、次のような実装になります。

```bash
#!/usr/bin/env bash

__VERSION__="1.0"
__AUTHOR__="Goichi (iisaka) Yukawa"
__ABOUT__="example using getopts"

MY_NAME=${$(basename $0)%.*}
# for macOS
GETOPT_EXE=/usr/local/Cellar/gnu-getopt/2.38.1/bin/getopt
PARSE_TMPFILE=/tmp/${MY_NAME}.$$.sh

CLEANUP() {
    [ -f ${PARSE_TMPFILE} ] && rm -f ${PARSE_TMPFILE}
}

trap CLEANUP HUP INT QUIT TERM EXIT

VERSION() {
cat <<_EOF_ 1>&2
${MY_NAME} - ${__ABOUT__}
_EOF_
}

USAGE() {
cat <<_EOF_ 1>&2
${MY_NAME} [OPTIONS] [SUBCOMMAND]
OPTIONS:
    --host <HOST>   hostname name
    --toekn <TOEN>  this option can be specified via an environment variable too
                    [env: ${MY_NAME}_TOKEN]
    --mode <MODE>   option with a certain set of possible values
                    [possible values: herbivore, carnivore, omnivore]
    -h|--help       print this message
    -V|--version    print version information
    -v|--verbose    verbosly output
SUBCOMMAND:
    help            Print this message or the help of the given subcommand(s)
_EOF_
}

BASE_OPTIONS="help,version,verbose"
LONG_OPTIONS=" -l ${BASE_OPTIONS},host:,token:,mode:"
SHORT_OPTIONS="-o h,V,v"

FLG_VERBOSE="NO"
OPT_HOST=""
OPT_TOKEN=""
OPT_MODE=""

DUMP_OPTIONS() {
[ "FLG_VERBOSE" != "NO" ] && {
cat <<_EOF_
FLG_VERBOSE=${FLG_VERBOSE}
OPT_HOST=${OPT_HOST}
OPT_TOKEN=${OPT_TOKEN}
OPT_MODE=${OPT_MODE}
_EOF_
}
}

Parse_Options() {
eval set -- "$@"

while true
do
    case "$1" in
    --host)            OPT_HOST="$2"  ; shift 2;;
    --token)           OPT_TOKEN="$2" ; shift 2;;
    -v|--verbose)      FLG_VERBOSE=1  ; shift ;;
    -h|--help)         USAGE ; exit 0 ;;
    -V|--version)      VERSION ; exit 0 ;;
    --)                break ;;
    esac
done
}

OPTIONS=$( ${GETOPT_EXE} ${SHORT_OPTIONS} ${LONG_OPTIONS} -- "$@" )
Parse_Options "${OPTIONS}" > ${PARSE_TMPFILE}

source ${PARSE_TMPFILE}
[ "${OPT_TOKEN}" != "" ] || {
     OPT_TOKEN=$(eval echo "$"${MY_NAME}_TOKEN)
}

case $1 in
help)  USAGE ; exit 0 ;;
esac
```

この方法は、ヘルプメッセージとパーサーの部分が物理的に離れてしまうだけでなく、　　
よく似たテキストを繰り返す必要があります。なにより、雛形とはいえオプションや引数が変わるたびに大幅なコード修正が必要になってしまいます。


## clap4shell を使った方法
[clap4shell](https://github.com/fumieval/clap4shell) は、Rustで実装された の clap ライブラリをベースにして getopts をよりモダンにしたコマンドラインのオプション解析をするためのCLIツールです。
clap4shellはオプション定義をYAML文書として標準入力から受け取り、解析結果を改行区切りのkey=value形式で表示し、評価することができます。

clap4shell は標準入力からオプション定義をしたYAMLドキュメント読み出すだけで、自身は何のオプションも持っていません。

次のようなYAMLでオプションを定義します。

```YAML
name: example
bin_name: $(basename $0)
version: "0.0"
about: sample text
author: Fumiaki Kinoshita <fumiexcel@gmail.com>
args:
  - verbose:
      help: verbose output
      short: v
      long: verbose
  - host:
      takes_value: true
      long: host
      value_name: <HOST>
      help: 'host name'
  - token:
        long: token
        help: this option can be specified via an environment variable too
        env: CLAP4SHELL_TOKEN
        takes_value: true
  - mode:
      long: mode
      help: option with a certain set of possible values
      possible_values: [ herbivore, carnivore, omnivore ]
  - cmd:
      help: command
  - arg:
      help: command arguments
      multiple_values: true
subcommands:
  - ls:
      about: Display a list of entities
      args:
        - entity:
            multiple_values: true
```

スキーマは [**clap_serde**](https://docs.rs/clap-serde/latest/clap_serde/) をベースにしています。

典型的な使い方は，シェルのヒアドキュメントとしてオプション定義を埋め込み，すべての引数をclap4shellに渡し，その出力を eval で評価します。

```
eval "$(clap4shell "$@" <<EOT
...
EOT
)"

case "$@" in
    -*)  ;; # may be option
    *) echo "subcommands: $@"
esac

# Print all variables
# declare -p | tail
```

サブコマンドは位置パラメーター（`$1, $2, ...`）として結合されます。

clap4shell が素晴らしいのは、ヘルプメッセージやバージョン情報を動的に生成してくれることです。

```Bassh
❯ ./example.sh --help
clap4shell: example 0.0
Fumiaki Kinoshita <fumiexcel@gmail.com>
sample text

USAGE:
    example.sh [OPTIONS] [ARGS] [SUBCOMMAND]

ARGS:
    <cmd>       command
    <arg>...    command arguments

OPTIONS:
    -h, --help             Print help information
        --host <<HOST>>    host name
        --mode <mode>      option with a certain set of possible values [possible values: herbivore,
                           carnivore, omnivore]
        --token <token>    this option can be specified via an environment variable too [env:
                           CLAP4SHELL_TOKEN=]
    -v, --verbose          verbose output
    -V, --version          Print version information

SUBCOMMANDS:
    clap4shell-completion    Generate an autocompletion script
    help                     Print this message or the help of the given subcommand(s)
    ls                       Display a list of entities
```


