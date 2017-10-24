import argparse

# parser의 인스턴스 작성
parser = argparse.ArgumentParser(description='Example command')
# 문자열을 받는 -s 옵션을 정의
parser.add_argument('-s', '--string', type=str, help='string to display', required=True)
# 수치를 받는 -n 옵션을 정의
parser.add_argument('-n', '--num', type=int, help='number of time repeatedly display the string', default=2)
# 인수를 해석(parse)하여 얻어진 값을 변수에 저장
args = parser.parse_args()

print(args.string * args.num)
