if [[ $1 == "" ]]
then
  python -m unittest caesaraiunit.AnthropicTestCase
else
  python -m unittest caesaraiunit.AnthropicTestCase.$1
fi