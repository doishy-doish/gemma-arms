"""ROULETTE stagea (DRY-RUN, not fired) — seed 7, pool v1.
Draw: S1=fastapi_14786, S2=fastapi_13537, S3=tornado_s3c, S4=fastapi_14258, S5=fastapi_15589, S6=pyramid_s6a.
Builder: scratch/roulette/roulette-build.js. Anchor fragments byte-verbatim from scratch/duck-6-stagea_6.py; candidate fragments pyDq-escaped from scratch/roulette/spec-*.json (round-trip verified).
"""
"""Duck stage-A PERSONA (reasoning low + terse lock + ORACLES exactness): same-6 clean-room, one turn each, then public-proxy score.
Model: tinfoil/gemma4-31b via browser rail (pure chat API, no harness in Duck).
Harness (checkout/apply/pytest) lives HERE, not in the API.
"""

"""TESTING-ONLY BUNDLE (not submittable) — what stays here and why it cannot ship:
- THIS FILE (+ duckapi_duckai.py rail driver) is OUR measurement instrument on
  GitHub Actions. Official grading runs THEIR harness (HARNESS_README:
  Container A agent -> git diff -> Container B hermetic pytest) over
  submission.zip. Nothing here transfers; similarity is behavioral at best.
- ORACLES (exact import lines, recipes, forbid-lists): per-task answer keys for
  calibration. A submission must be a general agent (single-model rule,
  declarative-only: agent.yaml/prompts/skills/adapters — no Python
  orchestration, no hardcoded per-task answers). Shipping oracles = overfit to
  6 tasks, scores ~0 on the hidden set.
- PINNED 6 (TASKS/SLICES/PYTESTS at fixed base commits + test patches): our
  private slice. Official eval = full hidden task set; this bundle covers none
  of it.
- RETRY/T2/REVISE LOOPS, verbose tails, FAIL_TAILS, MODFILE/SHADOW-GUARD: our
  diagnostic scaffolding and draw budget. Official budgets (calls/wall/
  compaction) are enforced server-side by their harness; our loop counts
  against nothing there and cannot be submitted (no Python entrypoints allowed).
- Duck.ai CHAT RAIL: test transport only (official = vLLM tool-calling on 4xL4; chat tricks don't transfer).
- PARALLEL-FIRE RULE: serial-depends-on-last may still fire in parallel at HIGH confidence (prior GREEN same SHA / mechanical byte-proof); gate is confidence, not order (M232).
Rule: instrument freely here (faithfulness-only: never relax tests, never touch
test files); the submission path takes only what transfers de-oracled.
"""
import asyncio, os, sys, subprocess, tarfile, threading, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from duckapi_duckai import DuckAISession

SLICES = {
    """fastapi_14786""": "from typing import Optional\n\n\ndef get_authorization_scheme_param(\n    authorization_header_value: Optional[str],\n) -> tuple[str, str]:\n    if not authorization_header_value:\n        return \"\", \"\"\n    scheme, _, param = authorization_header_value.partition(\" \")\n    return scheme, param\n",
    """fastapi_13537""": "def request_params_to_args(\n    fields: Sequence[ModelField],\n    received_params: Union[Mapping[str, Any], QueryParams, Headers],\n) -> Tuple[Dict[str, Any], List[Any]]:\n    values: Dict[str, Any] = {}\n    errors: List[Dict[str, Any]] = []\n\n    if not fields:\n        return values, errors\n\n    first_field = fields[0]\n    fields_to_extract = fields\n    single_not_embedded_field = False\n    default_convert_underscores = True\n    if len(fields) == 1 and lenient_issubclass(first_field.type_, BaseModel):\n        fields_to_extract = get_cached_model_fields(first_field.type_)\n        single_not_embedded_field = True\n        # If headers are in a Pydantic model, the way to disable convert_underscores\n        # would be with Header(convert_underscores=False) at the Pydantic model level\n        default_convert_underscores = getattr(\n            first_field.field_info, \"convert_underscores\", True\n        )\n\n    params_to_process: Dict[str, Any] = {}\n\n    processed_keys = set()\n\n    for field in fields_to_extract:\n        alias = None\n        if isinstance(received_params, Headers):\n            # Handle fields extracted from a Pydantic Model for a header, each field\n            # doesn't have a FieldInfo of type Header with the default convert_underscores=True\n            convert_underscores = getattr(\n                field.field_info, \"convert_underscores\", default_convert_underscores\n            )\n            if convert_underscores:\n                alias = (\n                    field.alias\n                    if field.alias != field.name\n                    else field.name.replace(\"_\", \"-\")\n                )\n        value = _get_multidict_value(field, received_params, alias=alias)\n        if value is not None:\n            params_to_process[field.name] = value\n        processed_keys.add(alias or field.alias)\n        processed_keys.add(field.name)\n\n    for key, value in received_params.items():\n        if key not in processed_keys:\n            params_to_process[key] = value\n\n    if single_not_embedded_field:\n        field_info = first_field.field_info\n        assert isinstance(field_info, (params.Param, temp_pydantic_v1_params.Param)), (\n            \"Params must be subclasses of Param\"\n        )\n        loc: Tuple[str, ...] = (field_info.in_.value,)\n        v_, errors_ = _validate_value_with_model_field(\n            field=first_field, value=params_to_process, values=values, loc=loc\n        )\n        return {first_field.name: v_}, errors_\n\n    for field in fields:\n        value = _get_multidict_value(field, received_params)\n        field_info = field.field_info\n        assert isinstance(field_info, (params.Param, temp_pydantic_v1_params.Param)), (\n            \"Params must be subclasses of Param\"\n        )\n        loc = (field_info.in_.value, field.alias)\n        v_, errors_ = _validate_value_with_model_field(\n            field=field, value=value, values=values, loc=loc\n        )\n        if errors_:\n            errors.extend(errors_)\n        else:\n            values[field.name] = v_\n    return values, errors\n\n\ndef is_union_of_base_models(field_type: Any) -> bool:\n    \"\"\"Check if field type is a Union where all members are BaseModel subclasses.\"\"\"\n    from fastapi.types import UnionType\n\n    origin = get_origin(field_type)\n\n    # Check if it's a Union type (covers both typing.Union and types.UnionType in Python 3.10+)\n    if origin is not Union and origin is not UnionType:\n        return False\n\n    union_args = get_args(field_type)\n\n    for arg in union_args:\n        if not _is_model_class(arg):\n            return False\n\n    return True\n\n\ndef _should_embed_body_fields(fields: List[ModelField]) -> bool:\n    if not fields:\n        return False\n    # More than one dependency could have the same field, it would show up as multiple\n    # fields but it's the same one, so count them by name\n    body_param_names_set = {field.name for field in fields}\n    # A top level field has to be a single field, not multiple\n    if len(body_param_names_set) > 1:\n        return True\n    first_field = fields[0]\n    # If it explicitly specifies it is embedded, it has to be embedded\n    if getattr(first_field.field_info, \"embed\", None):\n        return True\n    # If it's a Form (or File) field, it has to be a BaseModel (or a union of BaseModels) to be top level\n    # otherwise it has to be embedded, so that the key value pair can be extracted\n    if (\n        isinstance(first_field.field_info, (params.Form, temp_pydantic_v1_params.Form))\n        and not _is_model_class(first_field.type_)\n        and not is_union_of_base_models(first_field.type_)\n    ):\n        return True\n    return False\n\n\nasync def _extract_form_body(\n    body_fields: List[ModelField],\n    received_body: FormData,\n) -> Dict[str, Any]:\n    values = {}\n\n    for field in body_fields:\n        value = _get_multidict_value(field, received_body)\n        field_info = field.field_info\n        if (\n            isinstance(field_info, (params.File, temp_pydantic_v1_params.File))\n            and is_bytes_field(field)\n            and isinstance(value, UploadFile)\n        ):\n            value = await value.read()\n        elif (\n            is_bytes_sequence_field(field)\n            and isinstance(field_info, (params.File, temp_pydantic_v1_params.File))\n            and value_is_sequence(value)\n        ):\n            # For types\n            assert isinstance(value, sequence_types)  # type: ignore[arg-type]\n            results: List[Union[bytes, str]] = []\n\n            async def process_fn(\n                fn: Callable[[], Coroutine[Any, Any, Any]],\n            ) -> None:\n                result = await fn()\n                results.append(result)  # noqa: B023\n\n            async with anyio.create_task_group() as tg:\n                for sub_value in value:\n                    tg.start_soon(process_fn, sub_value.read)\n            value = serialize_sequence_value(field=field, value=results)\n        if value is not None:\n            values[field.alias] = value\n    for key, value in received_body.items():\n        if key not in values:\n            values[key] = value\n    return values\n\n\nasync def request_body_to_args(\n",
    """tornado_s3c""": "          try:\n              result = yield wait_iterator.next()\n          except Exception as e:\n              print(\"Error {} from {}\".format(e, wait_iterator.current_future))\n          else:\n              print(\"Result {} recieved from {} at {}\".format(\n                  result, wait_iterator.current_future,\n                  wait_iterator.current_index))\n\n    Because results are returned as soon as they are available the\n    output from the iterator *will not be in the same order as the\n    input arguments*. If you need to know which future produced the\n    current result, you can use the attributes\n    ``WaitIterator.current_future``, or ``WaitIterator.current_index``\n    to get the index of the future from the input list. (if keyword\n    arguments were used in the construction of the `WaitIterator`,\n    ``current_index`` will use the corresponding keyword).\n\n    .. versionadded:: 4.1\n    \"\"\"\n    def __init__(self, *args, **kwargs):\n        if args and kwargs:\n            raise ValueError(\n                \"You must provide args or kwargs, not both\")\n\n        if kwargs:\n            self._unfinished = dict((f, k) for (k, f) in kwargs.items())\n            futures = list(kwargs.values())\n        else:\n            self._unfinished = dict((f, i) for (i, f) in enumerate(args))\n            futures = args\n\n        self._finished = collections.deque()\n        self.current_index = self.current_future = None\n        self._running_future = None\n\n        self_ref = weakref.ref(self)\n        for future in futures:\n            future.add_done_callback(functools.partial(\n                self._done_callback, self_ref))\n\n    def done(self):\n        \"\"\"Returns True if this iterator has no more results.\"\"\"\n        if self._finished or self._unfinished:\n            return False\n        # Clear the 'current' values when iteration is done.\n        self.current_index = self.current_future = None\n        return True\n\n    def next(self):\n        \"\"\"Returns a `.Future` that will yield the next available result.\n\n        Note that this `.Future` will not be the same object as any of\n        the inputs.\n        \"\"\"\n        self._running_future = TracebackFuture()\n\n        if self._finished:\n            self._return_result(self._finished.popleft())\n\n        return self._running_future\n\n    @staticmethod\n    def _done_callback(self_ref, done):\n        self = self_ref()\n        if self is not None:\n            if self._running_future and not self._running_future.done():\n                self._return_result(done)\n            else:\n                self._finished.append(done)\n\n    def _return_result(self, done):\n        \"\"\"Called set the returned future's state that of the future\n        we yielded, and set the current future for the iterator.\n        \"\"\"\n        chain_future(done, self._running_future)\n\n        self.current_future = done\n        self.current_index = self._unfinished.pop(done)\n\n\nclass YieldPoint(object):\n    \"\"\"Base class for objects that may be yielded from the generator.\n\n    .. deprecated:: 4.0\n       Use `Futures <.Future>` instead.\n    \"\"\"\n    def start(self, runner):\n        \"\"\"Called by the runner after the generator has yielded.\n\n        No other methods will be called on this object before ``start``.\n        \"\"\"\n        raise NotImplementedError()\n\n    def is_ready(self):\n        \"\"\"Called by the runner to determine whether to resume the generator.\n\n        Returns a boolean; may be called more than once.\n        \"\"\"\n        raise NotImplementedError()\n\n    def get_result(self):\n        \"\"\"Returns the value to use as the result of the yield expression.\n\n        This method will only be called once, and only after `is_ready`\n        has returned true.\n        \"\"\"\n        raise NotImplementedError()\n\n\nclass Callback(YieldPoint):",
    """fastapi_14258""": "    ) -> None:\n        \"\"\"\n        Include another `APIRouter` in the same current `APIRouter`.\n\n        Read more about it in the\n        [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/).\n\n        ## Example\n\n        ```python\n        from fastapi import APIRouter, FastAPI\n\n        app = FastAPI()\n        internal_router = APIRouter()\n        users_router = APIRouter()\n\n        @users_router.get(\"/users/\")\n        def read_users():\n            return [{\"name\": \"Rick\"}, {\"name\": \"Morty\"}]\n\n        internal_router.include_router(users_router)\n        app.include_router(internal_router)\n        ```\n        \"\"\"\n        if prefix:\n            assert prefix.startswith(\"/\"), \"A path prefix must start with '/'\"\n            assert not prefix.endswith(\"/\"), (\n                \"A path prefix must not end with '/', as the routes will start with '/'\"\n            )\n        else:\n            for r in router.routes:\n                path = getattr(r, \"path\")  # noqa: B009\n                name = getattr(r, \"name\", \"unknown\")\n                if path is not None and not path:\n                    raise FastAPIError(\n                        f\"Prefix and path cannot be both empty (path operation: {name})\"\n                    )\n        if responses is None:\n            responses = {}\n        for route in router.routes:\n            if isinstance(route, APIRoute):\n                combined_responses = {**responses, **route.responses}\n                use_response_class = get_value_or_default(\n                    route.response_class,\n                    router.default_response_class,\n                    default_response_class,\n                    self.default_response_class,\n                )\n                current_tags = []\n                if tags:\n                    current_tags.extend(tags)\n                if route.tags:\n                    current_tags.extend(route.tags)\n                current_dependencies: list[params.Depends] = []\n                if dependencies:\n                    current_dependencies.extend(dependencies)\n                if route.dependencies:\n                    current_dependencies.extend(route.dependencies)\n                current_callbacks = []\n                if callbacks:\n                    current_callbacks.extend(callbacks)\n                if route.callbacks:\n                    current_callbacks.extend(route.callbacks)\n                current_generate_unique_id = get_value_or_default(\n                    route.generate_unique_id_function,\n                    router.generate_unique_id_function,\n                    generate_unique_id_function,\n                    self.generate_unique_id_function,\n                )\n                self.add_api_route(\n                    prefix + route.path,\n                    route.endpoint,\n                    response_model=route.response_model,\n                    status_code=route.status_code,\n                    tags=current_tags,\n",
    """fastapi_15589""": "def request_params_to_args(\n    fields: Sequence[ModelField],\n    received_params: Mapping[str, Any] | QueryParams | Headers,\n) -> tuple[dict[str, Any], list[Any]]:\n    values: dict[str, Any] = {}\n    errors: list[dict[str, Any]] = []\n\n    if not fields:\n        return values, errors\n\n    first_field = fields[0]\n    fields_to_extract = fields\n    single_not_embedded_field = False\n    default_convert_underscores = True\n    if len(fields) == 1 and lenient_issubclass(\n        first_field.field_info.annotation, BaseModel\n    ):\n        fields_to_extract = get_cached_model_fields(first_field.field_info.annotation)\n        single_not_embedded_field = True\n        # If headers are in a Pydantic model, the way to disable convert_underscores\n        # would be with Header(convert_underscores=False) at the Pydantic model level\n        default_convert_underscores = getattr(\n            first_field.field_info, \"convert_underscores\", True\n        )\n\n    params_to_process: dict[str, Any] = {}\n\n    processed_keys = set()\n\n    for field in fields_to_extract:\n        alias = None\n        if isinstance(received_params, Headers):\n            # Handle fields extracted from a Pydantic Model for a header, each field\n            # doesn't have a FieldInfo of type Header with the default convert_underscores=True\n            convert_underscores = getattr(\n                field.field_info, \"convert_underscores\", default_convert_underscores\n            )\n            if convert_underscores:\n                alias = get_validation_alias(field)\n                if alias == field.name:\n                    alias = alias.replace(\"_\", \"-\")\n        value = _get_multidict_value(field, received_params, alias=alias)\n        if value is not None:\n            params_to_process[get_validation_alias(field)] = value\n        processed_keys.add(alias or get_validation_alias(field))\n\n    for key in received_params.keys():\n        if key not in processed_keys:\n            if isinstance(received_params, (ImmutableMultiDict, Headers)):\n                value = received_params.getlist(key)\n                if isinstance(value, list) and (len(value) == 1):\n                    params_to_process[key] = value[0]\n                else:\n                    params_to_process[key] = value\n            else:\n                params_to_process[key] = received_params.get(key)\n\n    if single_not_embedded_field:\n        field_info = first_field.field_info\n        assert isinstance(field_info, params.Param), (\n            \"Params must be subclasses of Param\"\n        )\n        loc: tuple[str, ...] = (field_info.in_.value,)\n        v_, errors_ = _validate_value_with_model_field(\n            field=first_field, value=params_to_process, values=values, loc=loc\n        )\n        return {first_field.name: v_}, errors_\n\n    for field in fields:\n        value = _get_multidict_value(field, received_params)\n        field_info = field.field_info\n        assert isinstance(field_info, params.Param), (\n            \"Params must be subclasses of Param\"\n        )\n        loc = (field_info.in_.value, get_validation_alias(field))\n        v_, errors_ = _validate_value_with_model_field(\n            field=field, value=value, values=values, loc=loc\n        )\n        if errors_:\n            errors.extend(errors_)\n        else:\n            values[field.name] = v_\n    return values, errors\n\n\ndef is_union_of_base_models(field_type: Any) -> bool:\n",
    """pyramid_s6a""": "        passed, the ``_port`` value is assumed to have been passed as\n        ``443``.  Likewise, if ``_scheme`` is passed as ``http`` and\n        ``_port`` is not passed, the ``_port`` value is assumed to have been\n        passed as ``80``. To avoid this behavior, always explicitly pass\n        ``_port`` whenever you pass ``_scheme``.\n\n        If a keyword ``_app_url`` is present, it will be used as the\n        protocol/hostname/port/leading path prefix of the generated URL.\n        For example, using an ``_app_url`` of\n        ``http://example.com:8080/foo`` would cause the URL\n        ``http://example.com:8080/foo/fleeb/flub`` to be returned from\n        this function if the expansion of the route pattern associated\n        with the ``route_name`` expanded to ``/fleeb/flub``.  If\n        ``_app_url`` is not specified, the result of\n        ``request.application_url`` will be used as the prefix (the\n        default).\n\n        If both ``_app_url`` and any of ``_scheme``, ``_host``, or ``_port``\n        are passed, ``_app_url`` takes precedence and any values passed for\n        ``_scheme``, ``_host``, and ``_port`` will be ignored.\n\n        This function raises a :exc:`KeyError` if the URL cannot be\n        generated due to missing replacement names.  Extra replacement\n        names are ignored.\n\n        If the route object which matches the ``route_name`` argument has\n        a :term:`pregenerator`, the ``*elements`` and ``**kw``\n        arguments passed to this function might be augmented or changed.\n        \"\"\"\n        try:\n            reg = self.registry\n        except AttributeError:\n            reg = get_current_registry() # b/c\n        mapper = reg.getUtility(IRoutesMapper)\n        route = mapper.get_route(route_name)\n\n        if route is None:\n            raise KeyError('No such route named %s' % route_name)\n\n        if route.pregenerator is not None:\n            elements, kw = route.pregenerator(self, elements, kw)\n\n        anchor = ''\n        qs = ''\n        app_url = None\n        host = None\n        scheme = None\n        port = None\n\n        if '_query' in kw:\n            query = kw.pop('_query')\n            if query:\n                qs = '?' + urlencode(query, doseq=True)\n\n        if '_anchor' in kw:\n            anchor = kw.pop('_anchor')\n            anchor = native_(anchor, 'utf-8')\n            anchor = '#' + anchor\n\n        if '_app_url' in kw:\n            app_url = kw.pop('_app_url')\n\n        if '_host' in kw:\n            host = kw.pop('_host')\n\n        if '_scheme' in kw:\n            scheme = kw.pop('_scheme')\n\n        if '_port' in kw:\n            port = kw.pop('_port')\n\n        if app_url is None:\n            if (scheme is not None or host is not None or port is not None):\n                app_url = self._partial_application_url(scheme, host, port)\n            else:\n                app_url = self.application_url\n\n        path = route.generate(kw) # raises KeyError if generate fails\n\n        if elements:\n            suffix = _join_elements(elements)\n            if not path.endswith('/'):\n                suffix = '/' + suffix\n        else:\n            suffix = ''\n\n        return app_url + path + suffix + qs + anchor\n\n    def route_path(self, route_name, *elements, **kw):\n        \"\"\"\n        Generates a path (aka a 'relative URL', a URL minus the host, scheme,\n        and port) for a named :app:`Pyramid` :term:`route configuration`.\n\n        This function accepts the same argument as\n        :meth:`pyramid.request.Request.route_url` and performs the same duty.\n        It just omits the host, port, and scheme information in the return\n        value; only the script_name, path, query parameters, and anchor data\n        are present in the returned string.\n\n        For example, if you've defined a route named 'foobar' with the path\n        ``/{foo}/{bar}``, this call to ``route_path``::\n\n            request.route_path('foobar', foo='1', bar='2')\n\n        Will return the string ``/1/2``.\n",
}
ISSUES = {
    """fastapi_14786""": """ISSUE (fastapi_14786 in fastapi/fastapi at eacbce24c9d2):
Strip whitespaces from `Authorization` header credentials (RFC 6750 section 2.1).
Problem: get_authorization_scheme_param preserves leading/trailing whitespace in the credential, so `Authorization: Bearer   xxx` yields credentials `"  xxx"`.
Fix: return scheme, param.strip().
Tests: `Other  foobar ` -> ("Other", "foobar"); `Bearer  testtoken ` -> ("Bearer", "testtoken").""",
    """fastapi_13537""": """ISSUE (fastapi_13537 in fastapi/fastapi at 3b4b5ab8c819):
Form values with empty strings must be treated as missing (None default), for HTML-form compatibility. Regression from PR #12134.
Spec: `_get_multidict_value` uses None for both absent values and None defaults. `_extract_form_body` skips None values; a later pass re-adds missing fields from request params, but a form field set to "" is seen as absent, `_get_multidict_value` returns the None default (skipped in pass 1), then pass 2 finds "" in the params and adds it, and validation chokes on "".
Fix: track already-visited fields instead of relying on the values dict (as `request_params_to_args` already does). Keep the extra-key fix. Correct file only.
closes #13533""",
    """tornado_s3c""": "[ISSUE]\n**Title:** WaitIterator is Garbage Collected When No Strong Reference is Held, Leading to TimeoutError\n\n**Description:**\nWhen using `WaitIterator` without maintaining a strong reference to it, the iterator may be prematurely garbage collected. This causes the associated operation to never complete, resulting in a `TimeoutError`.\n\n**Example Code:**\n```python\nimport tornado.gen\nimport tornado.ioloop\nimport datetime\n\n@tornado.gen.coroutine\ndef example():\n    yield tornado.gen.with_timeout(\n        datetime.timedelta(seconds=0.1),\n        tornado.gen.WaitIterator(tornado.gen.sleep(0)).next()\n    )\n\ntornado.ioloop.IOLoop.current().run_sync(example)\n```\n\n**Expected Behavior:**\nThe `WaitIterator` should function correctly and complete the operation without requiring an external strong reference, preventing any timeout.\n\n**Actual Behavior:**\nA `TimeoutError` is raised because the `WaitIterator` is garbage collected before the operation can complete.\n[/ISSUE]",
    """fastapi_14258""": """ISSUE (fastapi_14258 in fastapi/fastapi at e94028ab60d1):
Show a clear error on attempt to include a router into itself: router.include_router(router) must raise AssertionError with the EXACT message: Cannot include the same APIRouter instance into itself. Did you mean to include a different router?
(The test uses match= on this exact string.)""",
    """fastapi_15589""": """ISSUE (fastapi_15589 in fastapi/fastapi at 22b02e26f9e8):
With convert_underscores=True (the default), underscore headers must NOT be accepted: only hyphen-separated header names validate; apps opt into underscores via convert_underscores=False.
Behavior: GET /header-requires-hyphen with both x-user-id=hyphenated-value AND x_user_id=underscore-value -> 200 {"x_user_id": "hyphenated-value"} (hyphen wins); with only x_user_id=underscore-value -> 422 with detail loc ["header", "x_user_id"].
Non-empty real fix required.""",
    """pyramid_s6a""": "[ISSUE]\n**Title:** `current_route_url()` Omits Query Parameters by Default\n\n**Description:**\nWhen generating a URL using `current_route_url()` without specifying the `_query` parameter, the resulting URL does not include the existing query parameters from the request. This leads to incomplete URLs that lack necessary query strings, causing unexpected behavior in routing and link generation.\n\n**Example Code:**\n```python\nfrom webob.multidict import GetDict\n\nrequest = create_mock_request()  # Assume this sets up a mock request\nrequest.GET = GetDict([('q', '123')], {})\nresult = request.current_route_url()\nprint(result)  # Outputs: 'http://example.com:5432/1/2/3'\n```\n\n**Expected Behavior:**\nThe `current_route_url()` method should include the query string from `request.GET` by default, resulting in:\n```\n'http://example.com:5432/1/2/3?q=123'\n```\n\n**Actual Behavior:**\nThe generated URL omits the query string, resulting in:\n```\n'http://example.com:5432/1/2/3'\n```\nThis omission prevents the application from recognizing and utilizing the query parameters as intended.\n[/ISSUE]",
}
CONTRACT = """OUTPUT CONTRACT (follow exactly):
- Output edit blocks only: no prose, no fences, no explanation.
- Each block has exactly this shape:
FILE: <exact repo-relative path>
<<<<<< SEARCH
<exact verbatim lines copied from LOCALIZED CODE>
======
<replacement lines>
>>>>>>
- SEARCH must occur in the target file byte-for-byte exactly once. Keep SEARCH minimal but unique (include enough surrounding context).
- Multiple SEARCH/======/>>>>>> pairs allowed under one FILE: header (one pair per hunk); every pair is matched independently, all must match.
- Minimal fix only.
"""
ALLOW = {
    """fastapi_14786""": ["""fastapi/security/utils.py"""],
    """fastapi_13537""": ["""fastapi/dependencies/utils.py"""],
    """tornado_s3c""": ["tornado/gen.py"],
    """fastapi_14258""": ["""fastapi/routing.py"""],
    """fastapi_15589""": ["""fastapi/dependencies/utils.py"""],
    """pyramid_s6a""": ["pyramid/url.py"],
}
PROMPTS = {}
for _pid in ISSUES:
    PROMPTS[_pid] = "You are an expert Python engineer. Minimal fix only.\n\n" + ISSUES[_pid] + "\n\nLOCALIZED CODE (verbatim from the base commit; SEARCH blocks must be copied from here byte-for-byte):\n" + SLICES[_pid] + "\n" + CONTRACT
TASKS = {
    """fastapi_14786""": {"repo": """fastapi/fastapi""", "base": """eacbce24c9d299c6a28110d9fc8ac50f53cddb08""", "test_patch": """--- a/tests/test_security_http_base.py
+++ b/tests/test_security_http_base.py
@@ -21,6 +21,12 @@ def test_security_http_base():
     assert response.json() == {"scheme": "Other", "credentials": "foobar"}
 
 
+def test_security_http_base_with_whitespaces():
+    response = client.get("/users/me", headers={"Authorization": "Other  foobar "})
+    assert response.status_code == 200, response.text
+    assert response.json() == {"scheme": "Other", "credentials": "foobar"}
+
+
 def test_security_http_base_no_credentials():
     response = client.get("/users/me")
     assert response.status_code == 401, response.text
--- a/tests/test_security_oauth2_authorization_code_bearer.py
+++ b/tests/test_security_oauth2_authorization_code_bearer.py
@@ -37,6 +37,12 @@ def test_token():
     assert response.json() == {"token": "testtoken"}
 
 
+def test_token_with_whitespaces():
+    response = client.get("/items", headers={"Authorization": "Bearer  testtoken "})
+    assert response.status_code == 200, response.text
+    assert response.json() == {"token": "testtoken"}
+
+
 def test_openapi_schema():
     response = client.get("/openapi.json")
     assert response.status_code == 200, response.text"""},
    """fastapi_13537""": {"repo": """fastapi/fastapi""", "base": """3b4b5ab8c819dce27fbaf0aa0a9c74b7f3255ec0""", "test_patch": """--- a/tests/test_form_default.py
+++ b/tests/test_form_default.py
@@ -0,0 +1,35 @@
+from typing import Optional
+
+from fastapi import FastAPI, File, Form
+from starlette.testclient import TestClient
+from typing_extensions import Annotated
+
+app = FastAPI()
+
+
+@app.post("/urlencoded")
+async def post_url_encoded(age: Annotated[Optional[int], Form()] = None):
+    return age
+
+
+@app.post("/multipart")
+async def post_multi_part(
+    age: Annotated[Optional[int], Form()] = None,
+    file: Annotated[Optional[bytes], File()] = None,
+):
+    return {"file": file, "age": age}
+
+
+client = TestClient(app)
+
+
+def test_form_default_url_encoded():
+    response = client.post("/urlencoded", data={"age": ""})
+    assert response.status_code == 200
+    assert response.text == "null"
+
+
+def test_form_default_multi_part():
+    response = client.post("/multipart", data={"age": ""})
+    assert response.status_code == 200
+    assert response.json() == {"file": None, "age": None}"""},
    """tornado_s3c""": {"repo": "tornadoweb/tornado", "base": "b450ff270df0", "test_patch": "@@ -1249,5 +1249,15 @@ def test_iterator(self):\n                     self.assertEqual(g.current_index, 3, 'wrong index')\n             i += 1\n \n+    @gen_test\n+    def test_no_ref(self):\n+        # In this usage, there is no direct hard reference to the\n+        # WaitIterator itself, only the Future it returns. Since\n+        # WaitIterator uses weak references internally to improve GC\n+        # performance, this used to cause problems.\n+        yield gen.with_timeout(datetime.timedelta(seconds=0.1),\n+                               gen.WaitIterator(gen.sleep(0)).next())\n+\n+\n if __name__ == '__main__':\n     unittest.main()"},
    """fastapi_14258""": {"repo": """fastapi/fastapi""", "base": """e94028ab60d18080810910352bc9129e8046c92d""", "test_patch": """--- a/tests/test_router_circular_import.py
+++ b/tests/test_router_circular_import.py
@@ -0,0 +1,12 @@
+import pytest
+from fastapi import APIRouter
+
+
+def test_router_circular_import():
+    router = APIRouter()
+
+    with pytest.raises(
+        AssertionError,
+        match="Cannot include the same APIRouter instance into itself. Did you mean to include a different router?",
+    ):
+        router.include_router(router)"""},
    """fastapi_15589""": {"repo": """fastapi/fastapi""", "base": """22b02e26f9e8c7e32bd8266e2b0ebe8bb3a0db2b""", "test_patch": """--- a/tests/test_query_cookie_header_model_extra_params.py
+++ b/tests/test_query_cookie_header_model_extra_params.py
@@ -11,6 +11,10 @@ class Model(BaseModel):
     model_config = {"extra": "allow"}
 
 
+class AuthHeaders(BaseModel):
+    x_user_id: str
+
+
 @app.get("/query")
 async def query_model_with_extra(data: Model = Query()):
     return data
@@ -26,6 +30,11 @@ async def cookies_model_with_extra(data: Model = Cookie()):
     return data
 
 
+@app.get("/header-requires-hyphen")
+async def header_model_requires_hyphen(data: AuthHeaders = Header()):
+    return data
+
+
 def test_query_pass_extra_list():
     client = TestClient(app)
     resp = client.get(
@@ -91,6 +100,32 @@ def test_header_pass_extra_single():
     assert resp_json["param2"] == "456"
 
 
+def test_header_model_prefers_hyphenated_header_with_convert_underscores():
+    client = TestClient(app)
+
+    resp = client.get(
+        "/header-requires-hyphen",
+        headers=[
+            ("x-user-id", "hyphenated-value"),
+            ("x_user_id", "underscore-value"),
+        ],
+    )
+
+    assert resp.status_code == 200
+    assert resp.json() == {"x_user_id": "hyphenated-value"}
+
+
+def test_header_model_rejects_underscore_header_with_convert_underscores():
+    client = TestClient(app)
+
+    resp = client.get(
+        "/header-requires-hyphen", headers={"x_user_id": "underscore-value"}
+    )
+
+    assert resp.status_code == 422
+    assert resp.json()["detail"][0]["loc"] == ["header", "x_user_id"]
+
+
 def test_cookie_pass_extra_list():
     client = TestClient(app)
     client.cookies = ["""},
    """pyramid_s6a""": {"repo": "Pylons/pyramid", "base": "159ef62eecd4ec6c5759720ca04d7c18f1d5fd8b", "test_patch": "--- a/pyramid/tests/test_url.py\n+++ b/pyramid/tests/test_url.py\n@@ -485,6 +485,34 @@ class TestURLMethodsMixin(unittest.TestCase):\n         self.assertEqual(result,\n                          'http://example.com:5432/1/2/3/extra1/extra2?a=1#foo')\n \n+    def test_current_route_url_with_request_query(self):\n+        from pyramid.interfaces import IRoutesMapper\n+        from webob.multidict import GetDict\n+        request = self._makeOne()\n+        request.GET = GetDict([('q', '123')], {})\n+        route = DummyRoute('/1/2/3')\n+        mapper = DummyRoutesMapper(route=route)\n+        request.matched_route = route\n+        request.matchdict = {}\n+        request.registry.registerUtility(mapper, IRoutesMapper)\n+        result = request.current_route_url()\n+        self.assertEqual(result,\n+                         'http://example.com:5432/1/2/3?q=123')\n+\n+    def test_current_route_url_with_query_override(self):\n+        from pyramid.interfaces import IRoutesMapper\n+        from webob.multidict import GetDict\n+        request = self._makeOne()\n+        request.GET = GetDict([('q', '123')], {})\n+        route = DummyRoute('/1/2/3')\n+        mapper = DummyRoutesMapper(route=route)\n+        request.matched_route = route\n+        request.matchdict = {}\n+        request.registry.registerUtility(mapper, IRoutesMapper)\n+        result = request.current_route_url(_query={'a':1})\n+        self.assertEqual(result,\n+                         'http://example.com:5432/1/2/3?a=1')\n+\n     def test_current_route_path(self):\n         from pyramid.interfaces import IRoutesMapper\n         request = self._makeOne()"},
}
REWRITE_LOW_TERSE = {"model": "tinfoil/gemma4-31b", "reasoningEffort": "low"}
FILE_HINTS = {
    "fastapi_14786": "Edit ONLY fastapi/security/utils.py (get_authorization_scheme_param, add .strip()).",
    "fastapi_13537": "Edit ONLY fastapi/dependencies/utils.py (_extract_form_body / visited fields + extra-key fix). Do NOT touch fastapi/routing.py.",
    """tornado_s3c""": "",
    "fastapi_14258": "Edit ONLY fastapi/routing.py (APIRouter.include_router self-guard, AssertionError).",
    "fastapi_15589": "Edit ONLY fastapi/dependencies/utils.py (query/cookie/header model extra params). Output a REAL diff, never empty.",
    """pyramid_s6a""": "",
}
EDGE_HINTS = {
    "fastapi_14786": "Must return scheme, param.strip().",
    "fastapi_13537": "Track visited fields, keep extra-key fix, correct file only.",
    """tornado_s3c""": "",
    "fastapi_14258": "Raise AssertionError with exact message on router.include_router(router).",
    "fastapi_15589": "Non-empty diff required; empty output = FAIL, retry.",
    """pyramid_s6a""": "",
}
ORACLES = {
    "fastapi_14786": "ORACLE: return scheme, param.strip().",
    "fastapi_13537": "ORACLE: track visited fields; extra keys pass through; correct file only.",
    """tornado_s3c""": "",
    "fastapi_14258": "ORACLE: raise AssertionError with EXACT message: Cannot include the same APIRouter instance into itself. Did you mean to include a different router? (test uses match= on this string).",
    "fastapi_15589": "ORACLE: mark BOTH the converted alias and the original field alias as processed (gold adds processed_keys for the lookup alias AND get_validation_alias(field)); non-empty diff required; empty output = FAIL.",
    """pyramid_s6a""": "",
}
def _parse_blocks(body):
    # SLICE-2 delimiter tolerance: models wrap blocks in fences and vary
    # chevrons/spacing (<<<< SEARCH, <<<<<<< SEARCH). Flex ONLY delimiter
    # lines via regex; SEARCH/repl CONTENT bytes stay exact (fidelity gate
    # lives in harness). A trailing ``` fence line is ignored.
    import re as _rx
    _SEARCH_RE = _rx.compile(r"^\s*<{4,8}\s*SEARCH\s*$")
    _SEP_RE = _rx.compile(r"^\s*={4,8}\s*$")
    _END_RE = _rx.compile(r"^\s*>{4,8}\s*$")
    blocks = []
    parts = body.split("FILE:")
    if len(parts) < 2:
        return None
    for p in parts[1:]:
        nl = p.find("\n")
        if nl < 0:
            return None
        path = p[:nl].strip().strip("`").strip()
        if not path:
            return None
        lines = p[nl + 1:].split("\n")
        while lines and lines[-1].strip() in ("```",):
            lines.pop()
        # MULTI-PAIR (M518): successive SEARCH/======/>>>>>> triples under one
        # FILE: header all apply; a malformed triple voids the whole reply.
        triples = []
        i = 0
        n = len(lines)
        while True:
            while i < n and not lines[i].strip():
                i += 1
            if i >= n:
                break
            if not _SEARCH_RE.match(lines[i]):
                return None
            try:
                mi = next(j for j in range(i + 1, n) if _SEP_RE.match(lines[j]))
                ei = next(j for j in range(mi + 1, n) if _END_RE.match(lines[j]))
            except StopIteration:
                return None
            if mi <= i + 1 or ei <= mi + 1:
                return None
            search = "\n".join(lines[i + 1:mi])
            repl = "\n".join(lines[mi + 1:ei])
            if len(search.strip()) < 20:
                return None
            triples.append((search, repl))
            i = ei + 1
        if not triples:
            return None
        for (search, repl) in triples:
            blocks.append((path, search, repl))
    return blocks or None

async def ask(s, pid, prompt):
    full = CONTRACT + " Emit exactly ONE FILE:/SEARCH/REPLACE triple; SEARCH must be a verbatim copy of source lines (full signature, no truncation) or the reply voids.\n\n" + prompt
    last = ""
    for attempt in range(3):
        q = full if attempt == 0 else "INVALID prior output (unparseable block, wrong FILE, or ambiguous SEARCH). Resubmit BLOCKS ONLY, correct FILE, SEARCH copied verbatim from LOCALIZED CODE.\n\n" + full
        reply = await s.send(q, rewrite=REWRITE_LOW_TERSE)
        last = reply
        b = reply.strip()
        if b.startswith("```"):
            ls = b.split("\n")
            b = "\n".join(ls[1:-1] if ls[-1].strip().startswith("```") else ls[1:])
        bl = _parse_blocks(b)
        if bl and all(p in ALLOW.get(pid, []) for (p, _s, _r) in bl):
            return reply.replace("```", "")
        print("RETRY " + pid + " attempt=" + str(attempt + 1) + " len=" + str(len(reply)), flush=True)
    return last

_DEPS_OK = False
_DEPS_LOCK = threading.Lock()
PYTESTS = {
    "fastapi_14786": "tests/test_security_http_base.py",
    "fastapi_13537": "tests/test_form_default.py",
    """tornado_s3c""": "tornado/test/gen_test.py -k test_no_ref",
    "fastapi_14258": "tests/test_router_circular_import.py",
    "fastapi_15589": "tests/test_query_cookie_header_model_extra_params.py",
    """pyramid_s6a""": "tests/test_url.py -k \"test_current_route_url_with_request_query or test_current_route_url_with_query_override\"",
}
def ensure_deps():
    global _DEPS_OK
    with _DEPS_LOCK:
        if _DEPS_OK:
            return
        # DO NOT REMOVE annotated-doc (M495): fastapi runtime dep (`from annotated_doc import Doc`
        # in fastapi src). Agent never emits it; eval image has it baked. Without it every
        # pytest dies at collection (0/6 verified). Harness-only line (runners are online);
        # the submission bundle itself must still assume offline (M495a).
        sh("pip install -q fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2 2>&1 | tail -1", timeout=300)
        sh("pip install -q tornado pyramid webtest 2>&1 | tail -1", timeout=300)
        _DEPS_OK = True


def sh(cmd, **kw):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=kw.get("timeout", 300))
    return p.returncode, (p.stdout or "")[-2000:] + (p.stderr or "")[-2000:]

# SLICE-2 Turn-2 feedback: harness records actionable failure tails here;
# main() sends at most ONE follow-up per pid in the same session.
FAIL_TAILS = {}
def harness(pid, reply, t):
    body = reply.strip()
    if body.startswith("```"):
        ls = body.split("\n")
        body = "\n".join(ls[1:-1] if ls[-1].strip().startswith("```") else ls[1:])
    blocks = _parse_blocks(body)
    if not blocks:
        print("EMPTY-DIFF " + pid + " len=" + str(len(body)), flush=True)
        FAIL_TAILS[pid] = "no parseable FILE:/SEARCH blocks in reply len=" + str(len(body)) + " — resubmit BLOCKS ONLY, SEARCH copied verbatim from LOCALIZED CODE slice"
        return "empty len=" + str(len(body))
    ok_paths = ALLOW.get(pid, [])
    for (path, _s, _r) in blocks:
        if path not in ok_paths:
            print("WRONG-FILE " + pid + " " + path, flush=True)
            FAIL_TAILS[pid] = "wrong FILE " + path + " — allowed: " + str(ok_paths); return "wrong-file " + path
    # SLICE-2 (M471): ALL collected outputs go to OUT_DIR only (blocks +
    # real unified diffs + replies + pytest tails). Work checkouts + tarballs
    # stay in /tmp/duck6_<pid> and are NEVER uploaded (prior /tmp/duck6_*
    # glob caught worktrees+tarballs = 146MB bloat; target <5MB).
    OUT_DIR = "/tmp/duck6_out"
    try:
        os.makedirs(OUT_DIR, exist_ok=True)
    except Exception:
        pass
    raw_path = OUT_DIR + "/" + pid + ".blocks"
    open(raw_path, "w").write(body if body.endswith("\n") else body + "\n")
    work = "/tmp/duck6_" + pid
    sh("rm -rf " + work + " && mkdir -p " + work)
    url = "https://github.com/" + t["repo"] + "/archive/" + t["base"] + ".tar.gz"
    print("FETCH " + pid + " " + url, flush=True)
    try:
        urllib.request.urlretrieve(url, work + "/src.tgz")
    except Exception as e:
        print("FETCH-FAIL " + pid + " " + str(e)[:200], flush=True)
        return "fetch-fail len=" + str(len(reply))
    sh("tar xzf " + work + "/src.tgz -C " + work + " --strip-components=1 && cd " + work + " && pip install -q -e . --no-deps 2>&1 | tail -1", timeout=300)
    ensure_deps()
    # SHADOW-GUARD (M518): src-layout repos (requests) are unimportable from the
    # tarball root via pytest path insertion, so tests would silently run against
    # site-packages instead of the patch. Force tarball-first via PYTHONPATH and
    # PROVE it by resolving the module file before pytest.
    mod = t["repo"].split("/")[1]
    pyenv = "PYTHONPATH=" + work + ":" + work + "/src"
    mrc, mout = sh("cd " + work + " && python -c \"open('conftest.py','w').write('import inspect as _i;_i.getargspec=getattr(_i,\"getargspec\",_i.getfullargspec)\n')\" && " + pyenv + " python -c \"import " + mod + "; print(" + mod + ".__file__)\" 2>&1 | tail -2", timeout=60)
    print("MODFILE " + pid + " " + mod + " " + mout[-160:], flush=True)
    if (work + "/") not in mout:
        FAIL_TAILS[pid] = "shadow import: " + mod + " resolves outside work dir (" + mout[-160:] + ") — tarball code would NOT run; fix PYTHONPATH/install before trusting pytest"
        return "shadow-fail " + mod
    applied = []
    origs = {}
    n_bl = len(blocks)
    for (path, search, repl) in blocks:
        fp = work + "/" + path
        try:
            content = open(fp).read()
        except Exception:
            print("READ-FAIL " + pid + " " + path, flush=True)
            return "read-fail " + path
        n = content.count(search)
        if n == 1:
            new_content = content.replace(search, repl, 1)
        elif n == 0:
            # SLICE-2 whitespace fallback: trailing-whitespace-insensitive
            # match, applied ONLY on a strictly unique line-range hit
            # (verified before replace). Still a miss otherwise.
            new_content = None
            olines = content.split("\n")
            norm = "\n".join(ln.rstrip() for ln in olines)
            nsearch = "\n".join(ln.rstrip() for ln in search.split("\n"))
            if nsearch.strip() and norm.count(nsearch) == 1:
                start = norm.find(nsearch)
                pre = norm[:start].count("\n")
                nlines = nsearch.count("\n") + 1
                if pre + nlines <= len(olines):
                    cand = "\n".join(olines[pre:pre + nlines])
                    if "\n".join(ln.rstrip() for ln in cand.split("\n")) == nsearch:
                        print("SEARCH-WSFALLBACK " + pid + " " + path + " lines=" + str(nlines), flush=True)
                        olines[pre:pre + nlines] = repl.split("\n")
                        new_content = "\n".join(olines)
            if new_content is None:
                print("SEARCH-MISS " + pid + " " + path + " n=0 block " + str(len(applied) + 1) + "/" + str(n_bl), flush=True)
                FAIL_TAILS[pid] = "SEARCH block " + str(len(applied) + 1) + "/" + str(n_bl) + " not found verbatim in " + path + " — copy exact lines from the LOCALIZED CODE slice (byte-for-byte, no rewording). NOTE: earlier blocks in this reply already applied to the file."
                return "search-miss " + path + " applied " + str(len(applied)) + "/" + str(n_bl)
        else:
            print("SEARCH-AMBIGUOUS " + pid + " " + path + " n=" + str(n) + " block " + str(len(applied) + 1) + "/" + str(n_bl), flush=True)
            FAIL_TAILS[pid] = "SEARCH block " + str(len(applied) + 1) + "/" + str(n_bl) + " matches " + str(n) + " places in " + path + " — extend SEARCH with more surrounding context lines until unique"
            return "search-ambiguous " + path + " applied " + str(len(applied)) + "/" + str(n_bl)
        origs[path] = content
        open(fp, "w").write(new_content)
        applied.append(path)
    # SLICE-2: real unified diffs into OUT_DIR (verdict evidence, not the
    # .blocks proposals — applied-file diff is what pytest actually ran).
    try:
        import difflib
        dl = []
        for path in applied:
            new = open(work + "/" + path).read()
            dl.extend(difflib.unified_diff(origs[path].splitlines(), new.splitlines(), "a/" + path, "b/" + path, lineterm=""))
        open(OUT_DIR + "/" + pid + ".diff", "w").write("\n".join(dl) + "\n" if dl else "")
    except Exception as e:
        print("DIFF-FAIL " + pid + " " + str(e)[:160], flush=True)
    rc, out = sh("cd " + work + " && python -m py_compile " + " ".join(sorted(set(applied))) + " 2>&1; echo COMPILE_RC=$?", timeout=60)
    print("COMPILE " + pid + " rc=" + str(rc) + " " + out[-200:], flush=True)
    open(work + "/test_patch.diff", "w").write(t["test_patch"] if t["test_patch"].endswith("\n") else t["test_patch"] + "\n")
    sh("cd " + work + " && git apply test_patch.diff 2>&1 | head -5; echo TEST_APPLIED_RC=$?", timeout=60)
    ensure_deps()
    tf = PYTESTS.get(pid, "")
    trc, tout = sh("cd " + work + " && " + pyenv + " python -m pytest " + tf + " -v --tb=short -W ignore::PendingDeprecationWarning -W ignore::DeprecationWarning -p no:cacheprovider > pytest_out.txt 2>&1; echo PYTEST_RC=$?; tail -15 pytest_out.txt", timeout=300)
    sh("cp " + work + "/pytest_out.txt " + OUT_DIR + "/" + pid + ".pytest.txt", timeout=30)
    import re as _re
    _m = _re.search(r"PYTEST_RC=(\d+)", tout)
    _ptr = _m.group(1) if _m else "?"
    print("TEST-RESULT " + pid + " rc=" + str(trc) + " pytest_rc=" + _ptr + " " + tout[-800:], flush=True)
    if str(_ptr) != "0":
        FAIL_TAILS[pid] = "pytest failed (pytest_rc=" + str(_ptr) + " blocks " + str(len(applied)) + "/" + str(n_bl) + "):\n" + tout[-1500:]
    print("APPLIED " + pid + " " + str(len(applied)) + "/" + str(n_bl) + " blocks", flush=True)
    return "collected len=" + str(len(reply)) + " testrc=" + _ptr + " blocks=" + str(len(applied)) + "/" + str(n_bl)

async def main():
    s = DuckAISession(model="tinfoil/gemma4-31b", timeout=240.0)
    results = {}
    replies = {}
    if True:  # (was try/finally-close; close moved after TURN-2)
        for pid, prompt in PROMPTS.items():
            t = TASKS[pid]
            print("=== TASK " + pid + " (" + t["repo"] + "@" + t["base"][:12] + ") ===", flush=True)
            try:
                reply = await ask(s, pid, prompt)
            except Exception as e:
                print("CHAT-FAIL " + pid + " " + str(e)[:300], flush=True)
                results[pid] = "chat-fail"
                continue
            print("REPLY-OK " + pid + " len=" + str(len(reply)), flush=True)
            replies[pid] = reply
            # SLICE-2: save the FULL raw reply (13920/14258 diagnosis needs
            # the unmodified model text, not just parsed blocks).
            try:
                os.makedirs("/tmp/duck6_out", exist_ok=True)
                open("/tmp/duck6_out/" + pid + ".reply.txt", "w").write(reply)
            except Exception as e:
                print("REPLY-SAVE-FAIL " + pid + " " + str(e)[:120], flush=True)
    # (no close here — session stays open for TURN-2 below; closed after)
    import asyncio as _a
    async def run_one(pid):
        return pid, await _a.to_thread(harness, pid, replies[pid], TASKS[pid])
    out = await _a.gather(*[run_one(pid) for pid in replies])
    for pid, res in out:
        results[pid] = res
        print("SCORED-COLLECTED " + pid + " " + res, flush=True)
    # TURN-2 (SLICE-2): ONE follow-up in the SAME session for actionable
    # harness failures only: pytest_rc=1 (real test failures, e.g. 7427
    # prelocalhost tail), search-miss, empty. Env/collection failures
    # (pytest_rc 2/4/5) are NOT model faults — no retry, no variance burn.
    try:
        t2pids = []
        for pid, res in out:
            if res.startswith("search-miss") or res.startswith("empty") or res.startswith("wrong-file"):
                t2pids.append(pid)
            elif "testrc=1" in res:
                t2pids.append(pid)
        for pid in t2pids:
            tail = FAIL_TAILS.get(pid, "")[-1500:]
            fb = ("HARNESS FEEDBACK on your prior BLOCKS for " + pid + ":\n" + tail
                  + "\nResubmit BLOCKS ONLY (same contract: FILE:/SEARCH/======/>>>>>>, SEARCH copied verbatim from LOCALIZED CODE). Minimal fix only.\n\n" + PROMPTS[pid])
            try:
                reply2 = await s.send(fb, rewrite=REWRITE_LOW_TERSE)
            except Exception as e:
                print("TURN2-FAIL " + pid + " " + str(e)[:200], flush=True)
                continue
            print("REPLY2-OK " + pid + " len=" + str(len(reply2)), flush=True)
            try:
                open("/tmp/duck6_out/" + pid + ".reply2.txt", "w").write(reply2)
            except Exception:
                pass
            res2 = await _a.to_thread(harness, pid, reply2, TASKS[pid])
            results[pid] = res2 + " [turn2]"
            print("SCORED-COLLECTED-T2 " + pid + " " + results[pid], flush=True)
    finally:
        await s.close()
    print("STAGEA-RESULTS " + str(results), flush=True)

asyncio.run(main())
