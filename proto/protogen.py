from grpc_tools import protoc

# Server
protoc.main((
    '',
    '-I.',
    '--python_out=../server',
    '--grpc_python_out=../server',
    './face.proto',
))

# Sample CLI
protoc.main((
    '',
    '-I.',
    '--python_out=../sample/cli',
    '--grpc_python_out=../sample/cli',
    './face.proto',
))
