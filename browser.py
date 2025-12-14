import socket
import ssl

class URL:
    def __init__(self, url=None):
        self.scheme, url = url.split("://",1)
        self.content = None

        if self.scheme in ["http", "https"]:
            if "/" not in url:
                url = url + "/"
            self.host, url = url.split("/",1)
            self.path = "/" + url

            if self.scheme == "http":
                self.port = 80
            elif self.scheme == "https":
                self.port = 443
            # URL에 포트가 지정되어 있는 경우
            if ":" in self.host:
                self.host, self.port = self.host.split(":",1)
                self.port = int(self.port)

        if self.scheme == "file":
            print("파일을 읽습니다.", url)
            if url.startswith("/") and ":" in url[1:3]:
                url = url[1:]

            with open(url, "r", encoding="utf-8") as f:
                self.content = f.read()

    def request(self):
        print("브라우저가 HTTP/1.1을 지원합니다. (연습용)")

        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, self.port))
        # ssl로 소켓을 감싸줌
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        request = build_http_request(
            method="GET",
            path=self.path,
            host=self.host,
            headers={
                "Connection": "close"
                # HTTP/1.1 에서 Keep-Alive 구현하지 않아도 되도록 응답 후 연결 끊기
                , "User-Agent": "MySimpleBrowser/0.1"
            }
        )
        s.send(request.encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ",2)
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            # 헤더는 대소문자 구분하지 않음
            response_headers[header.casefold()] = value.strip()

        # 헤더 정보를 통해 데이터 특수 형태 여부 확인
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        body = response.read()
        s.close()
        return body


def build_http_request(method, path, host, headers=None, body=None):
    if headers is None:
        headers = {}

    # HTTP/1.1 필수 헤더 기본값
    default_headers = {
        "Host": host,
        "Connection": "close",
        "User-Agent": "MyBrowser/0.1"
    }

    # 사용자 헤더가 기본값을 덮어쓰게
    default_headers.update(headers)

    # 요청 라인
    request_lines = [f"{method} {path} HTTP/1.1"]

    # 헤더 라인
    for key, value in default_headers.items():
        request_lines.append(f"{key}: {value}")

    # 헤더 종료를 의미하는 빈 줄
    request_lines.append("\r\n")

    # 바디가 있으면 추가
    if body:
        request_lines.append(body)

    return "\r\n".join(request_lines)

def show(body):
    if body is None:
        return
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    if url.scheme == "file":
        show(url.content)
    else:
        body = url.request()
        show(body)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # url 없이 요청할 경우 특정 로컬 파일 읽기
        url = "file:///C:/workspace-study/browser/README.md"
    load(URL(url))
