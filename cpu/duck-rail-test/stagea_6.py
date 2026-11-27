"""O4fix PYTESTS-scope for rich_3296 (vs O4 e65f8a7; one variable: single-node test scope; all 8 tasks byte-identical).
F5 ladder: A=14786/13537/14258/15589 + B=3905/3894 on anchor base (B3 owed; cite M575).
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
    """rich_3905""": "            return all(task.finished for task in self._tasks.values())\n\n    def start(self) -> None:\n        \"\"\"Start the progress display.\"\"\"\n        if not self.disable:\n            self.live.start(refresh=True)\n\n    def stop(self) -> None:\n        \"\"\"Stop the progress display.\"\"\"\n        self.live.stop()\n        if not self.console.is_interactive and not self.console.is_jupyter:\n            self.console.print()\n\n    def __enter__(self) -> Self:\n        self.start()\n        return self\n\n    def __exit__(\n        self,\n        exc_type: Optional[Type[BaseException]],\n        exc_val: Optional[BaseException],\n        exc_tb: Optional[TracebackType],\n    ) -> None:\n        self.stop()",
    """fastapi_14258""": "    ) -> None:\n        \"\"\"\n        Include another `APIRouter` in the same current `APIRouter`.\n\n        Read more about it in the\n        [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/).\n\n        ## Example\n\n        ```python\n        from fastapi import APIRouter, FastAPI\n\n        app = FastAPI()\n        internal_router = APIRouter()\n        users_router = APIRouter()\n\n        @users_router.get(\"/users/\")\n        def read_users():\n            return [{\"name\": \"Rick\"}, {\"name\": \"Morty\"}]\n\n        internal_router.include_router(users_router)\n        app.include_router(internal_router)\n        ```\n        \"\"\"\n        if prefix:\n            assert prefix.startswith(\"/\"), \"A path prefix must start with '/'\"\n            assert not prefix.endswith(\"/\"), (\n                \"A path prefix must not end with '/', as the routes will start with '/'\"\n            )\n        else:\n            for r in router.routes:\n                path = getattr(r, \"path\")  # noqa: B009\n                name = getattr(r, \"name\", \"unknown\")\n                if path is not None and not path:\n                    raise FastAPIError(\n                        f\"Prefix and path cannot be both empty (path operation: {name})\"\n                    )\n        if responses is None:\n            responses = {}\n        for route in router.routes:\n            if isinstance(route, APIRoute):\n                combined_responses = {**responses, **route.responses}\n                use_response_class = get_value_or_default(\n                    route.response_class,\n                    router.default_response_class,\n                    default_response_class,\n                    self.default_response_class,\n                )\n                current_tags = []\n                if tags:\n                    current_tags.extend(tags)\n                if route.tags:\n                    current_tags.extend(route.tags)\n                current_dependencies: list[params.Depends] = []\n                if dependencies:\n                    current_dependencies.extend(dependencies)\n                if route.dependencies:\n                    current_dependencies.extend(route.dependencies)\n                current_callbacks = []\n                if callbacks:\n                    current_callbacks.extend(callbacks)\n                if route.callbacks:\n                    current_callbacks.extend(route.callbacks)\n                current_generate_unique_id = get_value_or_default(\n                    route.generate_unique_id_function,\n                    router.generate_unique_id_function,\n                    generate_unique_id_function,\n                    self.generate_unique_id_function,\n                )\n                self.add_api_route(\n                    prefix + route.path,\n                    route.endpoint,\n                    response_model=route.response_model,\n                    status_code=route.status_code,\n                    tags=current_tags,\n",
    """fastapi_15589""": "def request_params_to_args(\n    fields: Sequence[ModelField],\n    received_params: Mapping[str, Any] | QueryParams | Headers,\n) -> tuple[dict[str, Any], list[Any]]:\n    values: dict[str, Any] = {}\n    errors: list[dict[str, Any]] = []\n\n    if not fields:\n        return values, errors\n\n    first_field = fields[0]\n    fields_to_extract = fields\n    single_not_embedded_field = False\n    default_convert_underscores = True\n    if len(fields) == 1 and lenient_issubclass(\n        first_field.field_info.annotation, BaseModel\n    ):\n        fields_to_extract = get_cached_model_fields(first_field.field_info.annotation)\n        single_not_embedded_field = True\n        # If headers are in a Pydantic model, the way to disable convert_underscores\n        # would be with Header(convert_underscores=False) at the Pydantic model level\n        default_convert_underscores = getattr(\n            first_field.field_info, \"convert_underscores\", True\n        )\n\n    params_to_process: dict[str, Any] = {}\n\n    processed_keys = set()\n\n    for field in fields_to_extract:\n        alias = None\n        if isinstance(received_params, Headers):\n            # Handle fields extracted from a Pydantic Model for a header, each field\n            # doesn't have a FieldInfo of type Header with the default convert_underscores=True\n            convert_underscores = getattr(\n                field.field_info, \"convert_underscores\", default_convert_underscores\n            )\n            if convert_underscores:\n                alias = get_validation_alias(field)\n                if alias == field.name:\n                    alias = alias.replace(\"_\", \"-\")\n        value = _get_multidict_value(field, received_params, alias=alias)\n        if value is not None:\n            params_to_process[get_validation_alias(field)] = value\n        processed_keys.add(alias or get_validation_alias(field))\n\n    for key in received_params.keys():\n        if key not in processed_keys:\n            if isinstance(received_params, (ImmutableMultiDict, Headers)):\n                value = received_params.getlist(key)\n                if isinstance(value, list) and (len(value) == 1):\n                    params_to_process[key] = value[0]\n                else:\n                    params_to_process[key] = value\n            else:\n                params_to_process[key] = received_params.get(key)\n\n    if single_not_embedded_field:\n        field_info = first_field.field_info\n        assert isinstance(field_info, params.Param), (\n            \"Params must be subclasses of Param\"\n        )\n        loc: tuple[str, ...] = (field_info.in_.value,)\n        v_, errors_ = _validate_value_with_model_field(\n            field=first_field, value=params_to_process, values=values, loc=loc\n        )\n        return {first_field.name: v_}, errors_\n\n    for field in fields:\n        value = _get_multidict_value(field, received_params)\n        field_info = field.field_info\n        assert isinstance(field_info, params.Param), (\n            \"Params must be subclasses of Param\"\n        )\n        loc = (field_info.in_.value, get_validation_alias(field))\n        v_, errors_ = _validate_value_with_model_field(\n            field=field, value=value, values=values, loc=loc\n        )\n        if errors_:\n            errors.extend(errors_)\n        else:\n            values[field.name] = v_\n    return values, errors\n\n\ndef is_union_of_base_models(field_type: Any) -> bool:\n",
    """rich_3894""": "    def __rich__(self) -> Panel:\n        return Panel.fit(\n            Group(*self._render()),\n            title=self.title,\n            border_style=\"scope.border\",\n            padding=(0, 1),\n        )\n\n    def _get_signature(self, name: str, obj: Any) -> Optional[Text]:\n        \"\"\"Get a signature for a callable.\"\"\"\n        try:\n            _signature = str(signature(obj)) + \":\"\n        except ValueError:\n            _signature = \"(...)\"\n        except TypeError:\n            return None\n\n        source_filename: Optional[str] = None\n        try:\n            source_filename = getfile(obj)\n        except (OSError, TypeError):\n            # OSError is raised if obj has no source file, e.g. when defined in REPL.\n            pass\n\n        callable_name = Text(name, style=\"inspect.callable\")\n        if source_filename:\n            callable_name.stylize(f\"link file://{source_filename}\")\n        signature_text = self.highlighter(_signature)\n\n        qualname = name or getattr(obj, \"__qualname__\", name)\n\n        # If obj is a module, there may be classes (which are callable) to display\n        if inspect.isclass(obj):\n            prefix = \"class\"\n        elif inspect.iscoroutinefunction(obj):\n            prefix = \"async def\"",
    """rich_2725""": "    def _render(\n        self, console: \"Console\", options: \"ConsoleOptions\", widths: List[int]\n    ) -> \"RenderResult\":\n        table_style = console.get_style(self.style or \"\")\n\n        border_style = table_style + console.get_style(self.border_style or \"\")\n        _column_cells = (\n            self._get_cells(console, column_index, column)\n            for column_index, column in enumerate(self.columns)\n        )\n        row_cells: List[Tuple[_Cell, ...]] = list(zip(*_column_cells))\n        _box = (\n            self.box.substitute(\n                options, safe=pick_bool(self.safe_box, console.safe_box)\n            )\n            if self.box\n            else None\n        )\n        _box = _box.get_plain_headed_box() if _box and not self.show_header else _box\n\n        new_line = Segment.line()\n\n        columns = self.columns\n        show_header = self.show_header\n        show_footer = self.show_footer\n        show_edge = self.show_edge\n        show_lines = self.show_lines\n        leading = self.leading\n\n        _Segment = Segment\n        if _box:\n            box_segments = [\n                (\n                    _Segment(_box.head_left, border_style),\n                    _Segment(_box.head_right, border_style),\n                    _Segment(_box.head_vertical, border_style),\n                ),\n                (\n                    _Segment(_box.foot_left, border_style),\n                    _Segment(_box.foot_right, border_style),\n                    _Segment(_box.foot_vertical, border_style),\n                ),\n                (\n                    _Segment(_box.mid_left, border_style),\n                    _Segment(_box.mid_right, border_style),\n                    _Segment(_box.mid_vertical, border_style),\n                ),\n            ]\n            if show_edge:\n                yield _Segment(_box.get_top(widths), border_style)\n                yield new_line\n        else:\n            box_segments = []",
    """rich_3296""": "        self, console: \"Console\", options: \"ConsoleOptions\"\n    ) -> \"Measurement\":\n        _, right, _, left = Padding.unpack(self.padding)\n        padding = left + right\n        if self.code_width is not None:\n            width = self.code_width + self._numbers_column_width + padding + 1\n            return Measurement(self._numbers_column_width, width)\n        lines = self.code.splitlines()\n        width = (\n            self._numbers_column_width\n            + padding\n            + (max(cell_len(line) for line in lines) if lines else 0)\n        )\n        if self.line_numbers:\n            width += 1\n        return Measurement(self._numbers_column_width, width)\n\n    def __rich_console__(\n        self, console: Console, options: ConsoleOptions\n    ) -> RenderResult:\n        segments = Segments(self._get_syntax(console, options))\n        if self.padding:\n            yield Padding(\n                segments, style=self._theme.get_background_style(), pad=self.padding\n            )\n        else:\n            yield segments\n\n    def _get_syntax(\n        self,\n        console: Console,\n        options: ConsoleOptions,\n    ) -> Iterable[Segment]:\n        \"\"\"\n        Get the Segments for the Syntax object, excluding any vertical/horizontal padding\n        \"\"\"\n        transparent_background = self._get_base_style().transparent_background\n        code_width = (\n            (\n                (options.max_width - self._numbers_column_width - 1)",
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
    """rich_3905""": "ISSUE (rich_3905 in Textualize/rich at 96dd4b60e3a7): Disabled Progress must print nothing on non-interactive consoles. Problem: stop() prints unconditionally when non-interactive, leaving a blank line even when disable=True. Fix: gate on disable first (symmetric start/stop). Tests: disabled non-interactive track emits empty string.",
    """fastapi_14258""": """ISSUE (fastapi_14258 in fastapi/fastapi at e94028ab60d1):
Show a clear error on attempt to include a router into itself: router.include_router(router) must raise AssertionError with the EXACT message: Cannot include the same APIRouter instance into itself. Did you mean to include a different router?
(The test uses match= on this exact string.)""",
    """fastapi_15589""": """ISSUE (fastapi_15589 in fastapi/fastapi at 22b02e26f9e8):
With convert_underscores=True (the default), underscore headers must NOT be accepted: only hyphen-separated header names validate; apps opt into underscores via convert_underscores=False. The Headers branch of request_params_to_args derives TWO keys per field -- the lookup alias and get_validation_alias(field) -- but records only one in processed_keys; unrecorded keys fall through to the extra-params loop.
Behavior: GET /header-requires-hyphen with both x-user-id=hyphenated-value AND x_user_id=underscore-value -> 200 {"x_user_id": "hyphenated-value"} (hyphen wins); with only x_user_id=underscore-value -> 422 with detail loc ["header", "x_user_id"].
Non-empty real fix required; aim the fix at the Headers-branch key bookkeeping.""",
    """rich_3894""": "ISSUE (rich_3894 in Textualize/rich at 4d6d631a3d2d): inspect() crashes on unusual __qualname__ (non-str, e.g. lru_cache + __slots__). Fix: isinstance check, fall back to __name__ then name. Tests: test_qualname_in_slots passes without exception.",
    """rich_2725""": "ISSUE (rich_2725 in Textualize/rich at 577def22dd83): fix table rendering order of box elements.\n\nfix table rendering order of box elements\n\n## Description\n\n* Previously \"mid\" box elements appeared in last line of table (footer), while \"footer\" box elements appeared mid table body. Reversed that order so mid is truly mid, footer is truly footer.\n* Tested with:\n\n    ```\n    table.box.head_left = '1'\n    table.box.head_vertical = '2'\n    table.box.head_right = '3'\n\n    table.box.mid_left = '4'\n    table.box.mid_vertical = '5'\n    table.box.mid_right = '6'\n\n    table.box.foot_left = '7'\n    table.box.foot_vertical = '8'\n    table.box.foot_right = '9'\n    ```\n\n  After change, correct ordering:\n\n    ```\n    +--------------------------------------------------------------------------+\n    1Date        2Title                            2  Production2    Box Office3\n    |------------ --------------------------------- ------------ --------------|\n    4Dec 20, 20195Star Wars: The Rise of Skywalker 5$275,000,0005  $375,126,1186\n    4May 25, 20185Solo: A Star Wars Story          5$275,000,0005  $393,151,3476\n    7Dec 15, 20178Star Wars Ep. VIII: The Last Jedi8$262,000,0008$1,332,539,8899\n    +--------------------------------------------------------------------------+\n    ```\n\n* All non-skipped prior automated tests pass. No automated tests added. Unclear that additional test for box ordering would add proportionate value.",
    """rich_3296""": "ISSUE (rich_3296 in Textualize/rich at 0d7e598fe7ea): Overriding the background_color of Syntax drops the padding. Problem: __rich_console__ wraps the segments in Padding using the theme background style instead of the base style, so a background_color override does not extend into the padded area. Fix: build the Padding wrapper with the base style. Tests: test_background_color_override_includes_padding passes.",
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
    """rich_3905""": ["rich/progress.py"],
    """fastapi_14258""": ["""fastapi/routing.py"""],
    """fastapi_15589""": ["""fastapi/dependencies/utils.py"""],
    """rich_3894""": ["rich/_inspect.py"],
    """rich_2725""": ["rich/table.py"],
    """rich_3296""": ["""rich/syntax.py"""],
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
    """rich_3905""": {"repo": "Textualize/rich", "base": "96dd4b60e3a7", "test_patch": "diff --git a/tests/test_progress.py b/tests/test_progress.py\nindex 0be683c3ea..20f426a4cd 100644\n--- a/tests/test_progress.py\n+++ b/tests/test_progress.py\n@@ -565,6 +565,30 @@ def test_no_output_if_progress_is_disabled() -> None:\n     assert result == expected\n \n \n+def test_no_output_if_progress_is_disabled_non_interactive() -> None:\n+    console = Console(\n+        file=io.StringIO(),\n+        force_interactive=False,\n+        width=60,\n+        color_system=\"truecolor\",\n+        legacy_windows=False,\n+        _environ={},\n+    )\n+    progress = Progress(\n+        console=console,\n+        disable=True,\n+    )\n+    test = [\"foo\", \"bar\", \"baz\"]\n+    expected_values = iter(test)\n+    with progress:\n+        for value in progress.track(test, description=\"test\"):\n+            assert value == next(expected_values)\n+    result = console.file.getvalue()\n+    print(repr(result))\n+    expected = \"\"\n+    assert result == expected\n+\n+\n def test_open() -> None:\n     console = Console(\n         file=io.StringIO(),\n"},
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
    """rich_3894""": {"repo": "Textualize/rich", "base": "4d6d631a3d2d", "test_patch": "diff --git a/tests/test_inspect.py b/tests/test_inspect.py\nindex 3f6e5b9fe8..d6972fb5ed 100644\n--- a/tests/test_inspect.py\n+++ b/tests/test_inspect.py\n@@ -404,6 +404,19 @@ class Thing:\n     assert render(module, methods=True) == expected\n \n \n+def test_qualname_in_slots():\n+    from functools import lru_cache\n+\n+    @lru_cache\n+    class Klass:\n+        __slots__ = (\"__qualname__\",)\n+\n+    try:\n+        inspect(Klass)\n+    except Exception as e:\n+        assert False, f\"Class with __qualname__ in __slots__ shouldn't raise {e}\"\n+\n+\n @pytest.mark.parametrize(\n     \"special_character,expected_replacement\",\n     (\n"},
    """rich_2725""": {"repo": "Textualize/rich", "base": "577def22dd83", "test_patch": "--- a/tests/test_table.py\n+++ b/tests/test_table.py\n@@ -1,6 +1,7 @@\n # encoding=utf-8\n \n import io\n+from textwrap import dedent\n \n import pytest\n \n@@ -234,6 +235,134 @@ def test_section():\n     assert output == expected\n \n \n+@pytest.mark.parametrize(\n+    \"show_header,show_footer,expected\",\n+    [\n+        (\n+            False,\n+            False,\n+            dedent(\n+                \"\"\"\n+                abbbbbcbbbbbbbbbcbbbbcbbbbbd\n+                1Dec  2Skywalker2275M2375M 3\n+                4May  5Solo     5275M5393M 6\n+                ijjjjjkjjjjjjjjjkjjjjkjjjjjl\n+                7Dec  8Last Jedi8262M81333M9\n+                qrrrrrsrrrrrrrrrsrrrrsrrrrrt\n+                \"\"\"\n+            ).lstrip(),\n+        ),\n+        (\n+            True,\n+            False,\n+            dedent(\n+                \"\"\"\n+                abbbbbcbbbbbbbbbcbbbbcbbbbbd\n+                1Month2Nickname 2Cost2Gross3\n+                efffffgfffffffffgffffgfffffh\n+                4Dec  5Skywalker5275M5375M 6\n+                4May  5Solo     5275M5393M 6\n+                ijjjjjkjjjjjjjjjkjjjjkjjjjjl\n+                7Dec  8Last Jedi8262M81333M9\n+                qrrrrrsrrrrrrrrrsrrrrsrrrrrt\n+                \"\"\"\n+            ).lstrip(),\n+        ),\n+        (\n+            False,\n+            True,\n+            dedent(\n+                \"\"\"\n+                abbbbbcbbbbbbbbbcbbbbcbbbbbd\n+                1Dec  2Skywalker2275M2375M 3\n+                4May  5Solo     5275M5393M 6\n+                ijjjjjkjjjjjjjjjkjjjjkjjjjjl\n+                4Dec  5Last Jedi5262M51333M6\n+                mnnnnnonnnnnnnnnonnnnonnnnnp\n+                7MONTH8NICKNAME 8COST8GROSS9\n+                qrrrrrsrrrrrrrrrsrrrrsrrrrrt\n+                \"\"\"\n+            ).lstrip(),\n+        ),\n+        (\n+            True,\n+            True,\n+            dedent(\n+                \"\"\"\n+                abbbbbcbbbbbbbbbcbbbbcbbbbbd\n+                1Month2Nickname 2Cost2Gross3\n+                efffffgfffffffffgffffgfffffh\n+                4Dec  5Skywalker5275M5375M 6\n+                4May  5Solo     5275M5393M 6\n+                ijjjjjkjjjjjjjjjkjjjjkjjjjjl\n+                4Dec  5Last Jedi5262M51333M6\n+                mnnnnnonnnnnnnnnonnnnonnnnnp\n+                7MONTH8NICKNAME 8COST8GROSS9\n+                qrrrrrsrrrrrrrrrsrrrrsrrrrrt\n+                \"\"\"\n+            ).lstrip(),\n+        ),\n+    ],\n+)\n+def test_placement_table_box_elements(show_header, show_footer, expected):\n+    \"\"\"Ensure box drawing characters correctly positioned.\"\"\"\n+\n+    table = Table(\n+        box=box.ASCII, show_header=show_header, show_footer=show_footer, padding=0\n+    )\n+\n+    # content rows indicated by numerals, pure dividers by letters\n+    table.box.__dict__.update(\n+        top_left=\"a\",\n+        top=\"b\",\n+        top_divider=\"c\",\n+        top_right=\"d\",\n+        head_left=\"1\",\n+        head_vertical=\"2\",\n+        head_right=\"3\",\n+        head_row_left=\"e\",\n+        head_row_horizontal=\"f\",\n+        head_row_cross=\"g\",\n+        head_row_right=\"h\",\n+        mid_left=\"4\",\n+        mid_vertical=\"5\",\n+        mid_right=\"6\",\n+        row_left=\"i\",\n+        row_horizontal=\"j\",\n+        row_cross=\"k\",\n+        row_right=\"l\",\n+        foot_left=\"7\",\n+        foot_vertical=\"8\",\n+        foot_right=\"9\",\n+        foot_row_left=\"m\",\n+        foot_row_horizontal=\"n\",\n+        foot_row_cross=\"o\",\n+        foot_row_right=\"p\",\n+        bottom_left=\"q\",\n+        bottom=\"r\",\n+        bottom_divider=\"s\",\n+        bottom_right=\"t\",\n+    )\n+\n+    # add content - note headers title case, footers upper case\n+    table.add_column(\"Month\", \"MONTH\", width=5)\n+    table.add_column(\"Nickname\", \"NICKNAME\", width=9)\n+    table.add_column(\"Cost\", \"COST\", width=4)\n+    table.add_column(\"Gross\", \"GROSS\", width=5)\n+\n+    table.add_row(\"Dec\", \"Skywalker\", \"275M\", \"375M\")\n+    table.add_row(\"May\", \"Solo\", \"275M\", \"393M\")\n+    table.add_section()\n+    table.add_row(\"Dec\", \"Last Jedi\", \"262M\", \"1333M\")\n+\n+    console = Console(record=True, width=28)\n+    console.print(table)\n+    output = console.export_text()\n+    print(repr(output))\n+\n+    assert output == expected\n+\n+\n if __name__ == \"__main__\":\n     render = render_tables()\n     print(render)\n"},
    """rich_3296""": {"""repo""": """Textualize/rich""", """base""": """0d7e598fe7ea""", "test_patch": r'''
diff --git a/tests/test_syntax.py b/tests/test_syntax.py
index 37cc293eb4..bbd4c7a5cb 100644
--- a/tests/test_syntax.py
+++ b/tests/test_syntax.py
@@ -406,6 +406,23 @@ def test_syntax_measure():
     assert code.__rich_measure__(console, console.options) == Measurement(3, 24)
 
 
+def test_background_color_override_includes_padding():
+    """Regression test for https://github.com/Textualize/rich/issues/3295"""
+
+    syntax = Syntax(
+        "x = 1",
+        lexer="python",
+        padding=(1, 3),
+        background_color="red",
+    )
+    result = render(syntax)
+    print(repr(result))
+    assert (
+        result
+        == "\x1b[41m                                                                                                    \x1b[0m\n\x1b[41m   \x1b[0m\x1b[38;2;248;248;242;41mx\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;255;70;137;41m=\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;174;129;255;41m1\x1b[0m\x1b[41m                                                                                         \x1b[0m\x1b[41m   \x1b[0m\n\x1b[41m                                                                                                    \x1b[0m\n"
+    )
+
+
 if __name__ == "__main__":
     syntax = Panel.fit(
         Syntax(

'''},
}
REWRITE_LOW_TERSE = {"model": "tinfoil/gemma4-31b", "reasoningEffort": "low"}
FILE_HINTS = {
    "fastapi_14786": "Edit ONLY fastapi/security/utils.py (get_authorization_scheme_param, add .strip()).",
    "fastapi_13537": "Edit ONLY fastapi/dependencies/utils.py (_extract_form_body / visited fields + extra-key fix). Do NOT touch fastapi/routing.py.",
    """rich_3905""": "Edit ONLY rich/progress.py (Progress start/stop symmetry).",
    "fastapi_14258": "Edit ONLY fastapi/routing.py (APIRouter.include_router self-guard, AssertionError).",
    "fastapi_15589": "Edit ONLY fastapi/dependencies/utils.py (query/cookie/header model extra params). Output a REAL diff, never empty.",
    """rich_3894""": "Edit ONLY rich/_inspect.py (_get_signature qualname fallback).",
    """rich_2725""": "Edit ONLY rich/table.py (box mid/foot ordering in _render).",
    """rich_3296""": "Edit ONLY rich/syntax.py (__rich_console__ padding style).",
}
EDGE_HINTS = {
    "fastapi_14786": "Must return scheme, param.strip().",
    "fastapi_13537": "Track visited fields, keep extra-key fix, correct file only.",
    """rich_3905""": "Repro disabled non-interactive track first; symmetric gate.",
    "fastapi_14258": "Raise AssertionError with exact message on router.include_router(router).",
    "fastapi_15589": "Non-empty diff required; empty output = FAIL, retry.",
    """rich_3894""": "Repro lru_cache + __slots__ inspect first; type-check fallback.",
    """rich_2725""": "Repro box-order matrix first; mid-before-foot.",
    """rich_3296""": "Padding wrapper must use the base style, not the theme background style.",
}
ORACLES = {
    "fastapi_14786": "ORACLE: return scheme, param.strip().",
    "fastapi_13537": "ORACLE: track visited fields; extra keys pass through; correct file only.",
    """rich_3905""": "",
    "fastapi_14258": "ORACLE: raise AssertionError with EXACT message: Cannot include the same APIRouter instance into itself. Did you mean to include a different router? (test uses match= on this string).",
    "fastapi_15589": "ORACLE: mark BOTH the converted alias and the original field alias as processed (gold adds processed_keys for the lookup alias AND get_validation_alias(field)); non-empty diff required; empty output = FAIL.",
    """rich_3894""": "",
    """rich_2725""": "",
    """rich_3296""": "",
}
PROMPTS["fastapi_13537"] += "\n" + FILE_HINTS["fastapi_13537"]
PROMPTS["""rich_3894"""] += "\n" + FILE_HINTS["""rich_3894"""]
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
    """rich_3905""": "tests/test_progress.py -k test_no_output_if_progress_is_disabled_non_interactive",
    "fastapi_14258": "tests/test_router_circular_import.py",
    "fastapi_15589": "tests/test_query_cookie_header_model_extra_params.py",
    """rich_3894""": "tests/test_inspect.py -k test_qualname_in_slots",
    """rich_2725""": "tests/test_table.py -k test_placement_table_box_elements",
    """rich_3296""": "tests/test_syntax.py -k test_background_color_override_includes_padding",
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
        sh("pip install -q tornado pyramid webtest pygments 2>&1 | tail -1", timeout=300)
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
    open(work + "/conftest.py", "w").write("import inspect as _i\n_i.getargspec = getattr(_i, 'getargspec', _i.getfullargspec)\n")
    mrc, mout = sh("cd " + work + " && " + pyenv + " python -c \"import " + mod + "; print(" + mod + ".__file__)\" 2>&1 | tail -2", timeout=60)
    print("MODFILE " + pid + " " + mod + " " + mout[-160:], flush=True)
    if (work + "/") not in mout:
        FAIL_TAILS[pid] = "shadow import: " + mod + " resolves outside work dir (" + mout[-160:] + ") — tarball code would NOT run; fix PYTHONPATH/install before trusting pytest"
        return "shadow-fail " + mod
    allow0 = (ALLOW.get(pid, [""])[0] or "")
    fmod = allow0[:-3].replace("/", ".") if allow0.endswith(".py") else mod
    mrc2, mout2 = sh("cd " + work + " && " + pyenv + " python -c \"import " + fmod + "; print(" + fmod + ".__file__)\" 2>&1 | tail -2", timeout=60)
    print("MODFILE2 " + pid + " " + fmod + " " + mout2[-160:], flush=True)
    if (work + "/") not in mout2:
        FAIL_TAILS[pid] = "shadow import (file): " + fmod + " resolves outside work dir (" + mout2[-160:] + ") - tarball code would NOT run"
        return "shadow-fail-file " + fmod
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
