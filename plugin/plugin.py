import pytest
import websockets
from pathlib import Path
from typing import Optional
from vcr_code import _vcr_instance
from storage.storage import CassetteStorage
from model.config import VCRConfig


@pytest.fixture(scope="module", autouse=True)
def mock_websockets(request):
    """Global fixture that replaces websockets.connect with VCR proxy."""
    marker = request.node.get_closest_marker("vcr")
    if marker:
        print("[mock_websockets] 执行全局 websocket连接替换")
        original_connect = websockets.connect
        _vcr_instance.original_connect = original_connect
        websockets.connect = _vcr_instance.intercept

        yield

        print("[mock_websockets] 录制功能结束，恢复原始连接")
        websockets.connect = original_connect
    else:
        yield None


@pytest.fixture(scope="function")
def vcr_context(request):
    """Main fixture that handles VCR setup for each test."""
    marker = request.node.get_closest_marker("vcr")
    if not marker:
        return

    # Generate unique identifier for this test
    query = request.node.callspec.id if hasattr(request.node, "callspec") else request.node.name
    project_root: Optional[str] = None

    # Get project root from test parameters or fixture
    if hasattr(request, 'param') and 'project_root' in request.param:
        project_root = request.param['project_root']
    else:
        try:
            project_root = request.getfixturevalue('ws_vcr_project_root')
        except LookupError:
            project_root = None

    # Initialize storage
    storage = CassetteStorage(project_root=project_root)
    cassette_path = storage.find_cassette(query)

    # Determine record mode
    record_mode = marker.kwargs.get('ws_record_mode', 'once')
    should_record = False

    if record_mode in ['all', 'rewrite']:
        should_record = True
    elif record_mode == 'none':
        if cassette_path is None:
            raise FileNotFoundError(
                f"VCR 模式为回放模式，但是并没有找到相应的磁盘文件: {query}"
            )
    else:
        should_record = not bool(cassette_path)

    # Set up VCR mode
    if should_record:
        print(f"[vcr_context] 当前测试 {query}, 录制模式")
        _vcr_instance.set_record_mode(query, storage)
    else:
        print(f"[vcr_context] 当前测试 {query}, 回放模式")
        try:
            all_data = storage.load(cassette_path)
            _vcr_instance.set_playback_mode(query, storage, all_data)
        except Exception as e:
            print(f"[vcr_context] 加载录音带失败: {e}")
            raise

    yield True

    # Cleanup after test
    if _vcr_instance.mode == "record":
        print("[vcr_context] 录制结束，开始存储数据")
        _vcr_instance.save_recording()

    _vcr_instance.mode = 'idle'
    _vcr_instance.cleanup()







