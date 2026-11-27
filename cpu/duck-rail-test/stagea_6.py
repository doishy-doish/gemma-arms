# HOW THIS VEHICLE IS SUPPOSED TO BE WRITTEN (M724, durable just-in-case note).
# (1) Prompts reuse the proven CONTRACT constant VERBATIM (by reference, never paraphrased).
#     M723: a hand-assembled paraphrase dropped the machine-readable FILE:/SEARCH shape and
#     voided a full 6-slot rail (0/6 measured the prompt bug, not difficulty).
# (2) Any reply-parser change ships with a parse-smoke: golden sample (must score) +
#     adversarial prose (must void) through the SHIPPED parser path before push (M672/M723).
# (3) Dependencies are fleet-wide: a new pip/test package lands in the rail ensure_deps AND
#     every staged F2P PIPPKGS AND every staged rail copy, grep-verified same turn (M722:
#     per-vehicle patching let inline_snapshot/sqlalchemy kill slots after M709/M495 named them).
# (4) Evidence lines print the tool own rc (e.g. echo RC=$? right after the tool, before tail)
#     or a grep summary -- never the tail pipe own rc; asserts check FULL captured text (M666/M721e).
# (5) One variable per fire; pre-reg (predictions + kill rules) BEFORE staging (M632).
# Lineage: M717-M724. This header is comment-only and changes no behavior.
"""R6 return-to-6 (same-6 ladder on h5-t1only-b2 base 614d8def; 2725/3296 retired to comments; T2 net restored; M717).
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
# R6-M717 RETIRED SLICES rich_2725 — return-to-6 (same-6 ladder); line-count preserved.
# R6-M717 RETIRED SLICES rich_3296 — return-to-6 (same-6 ladder); line-count preserved.
    """rich_2725""": "    def _render(\n        self, console: \"Console\", options: \"ConsoleOptions\", widths: List[int]\n    ) -> \"RenderResult\":\n        table_style = console.get_style(self.style or \"\")\n\n        border_style = table_style + console.get_style(self.border_style or \"\")\n        _column_cells = (\n            self._get_cells(console, column_index, column)\n            for column_index, column in enumerate(self.columns)\n        )\n        row_cells: List[Tuple[_Cell, ...]] = list(zip(*_column_cells))\n        _box = (\n            self.box.substitute(\n                options, safe=pick_bool(self.safe_box, console.safe_box)\n            )\n            if self.box\n            else None\n        )\n        _box = _box.get_plain_headed_box() if _box and not self.show_header else _box\n\n        new_line = Segment.line()\n\n        columns = self.columns\n        show_header = self.show_header\n        show_footer = self.show_footer\n        show_edge = self.show_edge\n        show_lines = self.show_lines\n        leading = self.leading\n\n        _Segment = Segment\n        if _box:\n            box_segments = [\n                (\n                    _Segment(_box.head_left, border_style),\n                    _Segment(_box.head_right, border_style),\n                    _Segment(_box.head_vertical, border_style),\n                ),\n                (\n                    _Segment(_box.foot_left, border_style),\n                    _Segment(_box.foot_right, border_style),\n                    _Segment(_box.foot_vertical, border_style),\n                ),\n                (\n                    _Segment(_box.mid_left, border_style),\n                    _Segment(_box.mid_right, border_style),\n                    _Segment(_box.mid_vertical, border_style),\n                ),\n            ]\n            if show_edge:\n                yield _Segment(_box.get_top(widths), border_style)\n                yield new_line\n        else:\n            box_segments = []",
    """rich_3296""": "        self, console: \"Console\", options: \"ConsoleOptions\"\n    ) -> \"Measurement\":\n        _, right, _, left = Padding.unpack(self.padding)\n        padding = left + right\n        if self.code_width is not None:\n            width = self.code_width + self._numbers_column_width + padding + 1\n            return Measurement(self._numbers_column_width, width)\n        lines = self.code.splitlines()\n        width = (\n            self._numbers_column_width\n            + padding\n            + (max(cell_len(line) for line in lines) if lines else 0)\n        )\n        if self.line_numbers:\n            width += 1\n        return Measurement(self._numbers_column_width, width)\n\n    def __rich_console__(\n        self, console: Console, options: ConsoleOptions\n    ) -> RenderResult:\n        segments = Segments(self._get_syntax(console, options))\n        if self.padding:\n            yield Padding(\n                segments, style=self._theme.get_background_style(), pad=self.padding\n            )\n        else:\n            yield segments\n\n    def _get_syntax(\n        self,\n        console: Console,\n        options: ConsoleOptions,\n    ) -> Iterable[Segment]:\n        \"\"\"\n        Get the Segments for the Syntax object, excluding any vertical/horizontal padding\n        \"\"\"\n        transparent_background = self._get_base_style().transparent_background\n        code_width = (\n            (\n                (options.max_width - self._numbers_column_width - 1)",
    """fastapi_14794""": """    elif lenient_issubclass(type_annotation, WebSocket):\n        dependant.websocket_param_name = param_name\n        return True\n    elif lenient_issubclass(type_annotation, HTTPConnection):\n        dependant.http_connection_param_name = param_name\n        return True\n    elif lenient_issubclass(type_annotation, Response):\n        dependant.response_param_name = param_name\n        return True\n    elif lenient_issubclass(type_annotation, StarletteBackgroundTasks):\n        dependant.background_tasks_param_name = param_name\n        return True\n    elif lenient_issubclass(type_annotation, SecurityScopes):\n        dependant.security_scopes_param_name = param_name\n        return True\n    return None\n\n\n@dataclass\nclass ParamDetails:\n    type_annotation: Any\n    depends: Optional[params.Depends]\n    field: Optional[ModelField]\n\n\ndef analyze_param(\n    *,\n    param_name: str,\n    annotation: Any,\n    value: Any,\n    is_path_param: bool,\n) -> ParamDetails:\n    field_info = None\n    depends = None\n    type_annotation: Any = Any\n    use_annotation: Any = Any\n    if annotation is not inspect.Signature.empty:\n        use_annotation = annotation\n        type_annotation = annotation\n    # Extract Annotated info\n    if get_origin(use_annotation) is Annotated:\n        annotated_args = get_args(annotation)\n        type_annotation = annotated_args[0]\n        fastapi_annotations = [\n            arg\n            for arg in annotated_args[1:]\n            if isinstance(arg, (FieldInfo, params.Depends))\n        ]\n        fastapi_specific_annotations = [\n            arg\n            for arg in fastapi_annotations\n            if isinstance(\n                arg,\n                (\n                    params.Param,\n                    params.Body,\n                    params.Depends,\n                ),\n            )\n        ]\n        if fastapi_specific_annotations:\n            fastapi_annotation: Union[FieldInfo, params.Depends, None] = (\n                fastapi_specific_annotations[-1]\n            )\n        else:\n            fastapi_annotation = None\n        # Set default for Annotated FieldInfo\n        if isinstance(fastapi_annotation, FieldInfo):\n            # Copy `field_info` because we mutate `field_info.default` below.\n            field_info = copy_field_info(\n                field_info=fastapi_annotation,\n                annotation=use_annotation,\n            )\n            assert (\n                field_info.default == Undefined or field_info.default == RequiredParam\n            ), (\n                f\"`{field_info.__class__.__name__}` default value cannot be set in\"\n                f\" `Annotated` for {param_name!r}. Set the default value with `=` instead.\"\n            )\n            if value is not inspect.Signature.empty:\n                assert not is_path_param, \"Path parameters cannot have default values\"\n                field_info.default = value\n            else:\n                field_info.default = RequiredParam\n        # Get Annotated Depends\n        elif isinstance(fastapi_annotation, params.Depends):\n            depends = fastapi_annotation\n    # Get Depends from default value\n    if isinstance(value, params.Depends):\n        assert depends is None, (\n            \"Cannot specify `Depends` in `Annotated` and default value\"\n            f\" together for {param_name!r}\"\n        )\n        assert field_info is None, (\n            \"Cannot specify a FastAPI annotation in `Annotated` and `Depends` as a\"\n            f\" default value together for {param_name!r}\"\n        )\n        depends = value\n    # Get FieldInfo from default value\n    elif isinstance(value, FieldInfo):\n        assert field_info is None, (\n            \"Cannot specify FastAPI annotations in `Annotated` and default value\"\n            f\" together for {param_name!r}\"\n        )\n        field_info = value\n        if isinstance(field_info, FieldInfo):\n            field_info.annotation = type_annotation\n\n    # Get Depends from type annotation\n""" """    if depends is not None and depends.dependency is None:\n        # Copy `depends` before mutating it\n        depends = copy(depends)\n        depends = dataclasses.replace(depends, dependency=type_annotation)\n\n    # Handle non-param type annotations like Request\n    if lenient_issubclass(\n        type_annotation,\n        (\n            Request,\n            WebSocket,\n            HTTPConnection,\n            Response,\n            StarletteBackgroundTasks,\n            SecurityScopes,\n        ),\n    ):\n        assert depends is None, f\"Cannot specify `Depends` for type {type_annotation!r}\"\n        assert field_info is None, (\n            f\"Cannot specify FastAPI annotation for type {type_annotation!r}\"\n        )\n    # Handle default assignations, neither field_info nor depends was not found in Annotated nor default value\n    elif field_info is None and depends is None:\n        default_value = value if value is not inspect.Signature.empty else RequiredParam\n        if is_path_param:\n            # We might check here that `default_value is RequiredParam`, but the fact is that the same\n            # parameter might sometimes be a path parameter and sometimes not. See\n            # `tests/test_infer_param_optionality.py` for an example.\n            field_info = params.Path(annotation=use_annotation)\n        elif is_uploadfile_or_nonable_uploadfile_annotation(\n            type_annotation\n        ) or is_uploadfile_sequence_annotation(type_annotation):\n            field_info = params.File(annotation=use_annotation, default=default_value)\n        elif not field_annotation_is_scalar(annotation=type_annotation):\n            field_info = params.Body(annotation=use_annotation, default=default_value)\n        else:\n            field_info = params.Query(annotation=use_annotation, default=default_value)\n\n    field = None\n    # It's a field_info, not a dependency\n""",
    """fastapi_14485""": """def _get_flat_fields_from_params(fields: List[ModelField]) -> List[ModelField]:\n    if not fields:\n        return fields\n    first_field = fields[0]\n    if len(fields) == 1 and _is_model_class(first_field.type_):\n        fields_to_extract = get_cached_model_fields(first_field.type_)\n        return fields_to_extract\n    return fields\n\n\ndef get_flat_params(dependant: Dependant) -> List[ModelField]:\n    flat_dependant = get_flat_dependant(dependant, skip_repeats=True)\n    path_params = _get_flat_fields_from_params(flat_dependant.path_params)\n    query_params = _get_flat_fields_from_params(flat_dependant.query_params)\n    header_params = _get_flat_fields_from_params(flat_dependant.header_params)\n    cookie_params = _get_flat_fields_from_params(flat_dependant.cookie_params)\n    return path_params + query_params + header_params + cookie_params\n\n\ndef get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:\n    if sys.version_info >= (3, 10):\n        signature = inspect.signature(call, eval_str=True)\n    else:\n        signature = inspect.signature(call)\n    unwrapped = inspect.unwrap(call)\n    globalns = getattr(unwrapped, \"__globals__\", {})\n    typed_params = [\n        inspect.Parameter(\n            name=param.name,\n            kind=param.kind,\n            default=param.default,\n            annotation=get_typed_annotation(param.annotation, globalns),\n        )\n        for param in signature.parameters.values()\n    ]\n    typed_signature = inspect.Signature(typed_params)\n    return typed_signature\n\n\ndef get_typed_annotation(annotation: Any, globalns: Dict[str, Any]) -> Any:\n    if isinstance(annotation, str):\n        annotation = ForwardRef(annotation)\n        annotation = evaluate_forwardref(annotation, globalns, globalns)\n        if annotation is type(None):\n            return None\n    return annotation\n\n\ndef get_typed_return_annotation(call: Callable[..., Any]) -> Any:\n    if sys.version_info >= (3, 10):\n        signature = inspect.signature(call, eval_str=True)\n    else:\n        signature = inspect.signature(call)\n    unwrapped = inspect.unwrap(call)\n    annotation = signature.return_annotation\n\n    if annotation is inspect.Signature.empty:\n        return None\n\n    globalns = getattr(unwrapped, \"__globals__\", {})\n    return get_typed_annotation(annotation, globalns)\n\n\ndef get_dependant(""",
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
With convert_underscores=True (the default), underscore headers must NOT be accepted: only hyphen-separated header names validate; apps opt into underscores via convert_underscores=False.
Behavior: GET /header-requires-hyphen with both x-user-id=hyphenated-value AND x_user_id=underscore-value -> 200 {"x_user_id": "hyphenated-value"} (hyphen wins); with only x_user_id=underscore-value -> 422 with detail loc ["header", "x_user_id"].
Non-empty real fix required.""",
    """rich_3894""": "ISSUE (rich_3894 in Textualize/rich at 4d6d631a3d2d): inspect() crashes on unusual __qualname__ (non-str, e.g. lru_cache + __slots__). Fix: isinstance check, fall back to __name__ then name. Tests: test_qualname_in_slots passes without exception.",
# R6-M717 RETIRED ISSUES rich_2725 — return-to-6 (same-6 ladder); line-count preserved.
# R6-M717 RETIRED ISSUES rich_3296 — return-to-6 (same-6 ladder); line-count preserved.
    """rich_2725""": "ISSUE (rich_2725 in Textualize/rich at 577def22dd83): fix table rendering order of box elements.\n\nfix table rendering order of box elements\n\n## Description\n\n* Previously \"mid\" box elements appeared in last line of table (footer), while \"footer\" box elements appeared mid table body. Reversed that order so mid is truly mid, footer is truly footer.\n* Tested with:\n\n    ```\n    table.box.head_left = '1'\n    table.box.head_vertical = '2'\n    table.box.head_right = '3'\n\n    table.box.mid_left = '4'\n    table.box.mid_vertical = '5'\n    table.box.mid_right = '6'\n\n    table.box.foot_left = '7'\n    table.box.foot_vertical = '8'\n    table.box.foot_right = '9'\n    ```\n\n  After change, correct ordering:\n\n    ```\n    +--------------------------------------------------------------------------+\n    1Date        2Title                            2  Production2    Box Office3\n    |------------ --------------------------------- ------------ --------------|\n    4Dec 20, 20195Star Wars: The Rise of Skywalker 5$275,000,0005  $375,126,1186\n    4May 25, 20185Solo: A Star Wars Story          5$275,000,0005  $393,151,3476\n    7Dec 15, 20178Star Wars Ep. VIII: The Last Jedi8$262,000,0008$1,332,539,8899\n    +--------------------------------------------------------------------------+\n    ```\n\n* All non-skipped prior automated tests pass. No automated tests added. Unclear that additional test for box ordering would add proportionate value.",
    """rich_3296""": "ISSUE (rich_3296 in Textualize/rich at 0d7e598fe7ea): Overriding the background_color of Syntax drops the padding. Problem: __rich_console__ wraps the segments in Padding using the theme background style instead of the base style, so a background_color override does not extend into the padded area. Fix: build the Padding wrapper with the base style. Tests: test_background_color_override_includes_padding passes.",
    """fastapi_14794""": """ISSUE (fastapi_14794 in fastapi/fastapi at 464c359bb03f):
Using Response as a dependency annotation fails: analyze_param() applies Response special-type handling before checking for Depends, raising "AssertionError: Cannot specify Depends for type Response" (starlette Response). Breaks Annotated[Response, Depends(modify_response)] and Response defaults.
Fix: in analyze_param(), check for Depends before applying Response special handling; when Depends is present, call the dependency normally and use its return value. Correct file only: fastapi/dependencies/utils.py.
Tests: test_response_with_depends_annotated (plus 6 more in tests/test_response_dependency.py) passes.""",
    """fastapi_14485""": """ISSUE (fastapi_14485 in fastapi/fastapi at 60699f306b67):",
"Stringified annotations under `if TYPE_CHECKING` never evaluate: get_typed_signature eval_str=True raises NameError on ForwardRef, so test_stringified_annotation_dependency fails (14464/14484).",
"Fix: add _get_signature helper (try eval_str=True, fall back to plain signature on NameError); use it in get_typed_signature + get_typed_return_annotation. Correct file only: fastapi/dependencies/utils.py.",
"Tests: test_get + test_openapi_schema in tests/test_stringified_annotation_dependency.py pass.""",
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
# R6-M717 RETIRED ALLOW rich_2725 — return-to-6 (same-6 ladder); line-count preserved.
# R6-M717 RETIRED ALLOW rich_3296 — return-to-6 (same-6 ladder); line-count preserved.
    """rich_2725""": ["rich/table.py"],
    """rich_3296""": ["""rich/syntax.py"""],
    """fastapi_14794""": ["""fastapi/dependencies/utils.py"""],
    """fastapi_14485""": ["""fastapi/dependencies/utils.py"""],
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
# R6-M717 RETIRED TASKS rich_2725 — return-to-6 (same-6 ladder); line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 1/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 2/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 3/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 4/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 5/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 6/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 7/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 8/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 9/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 10/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 11/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 12/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 13/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 14/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 15/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 16/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 17/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 18/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 19/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 20/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 21/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 22/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 23/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 24/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 25/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 26/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 27/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 28/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 29/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 30/31 — return-to-6; line-count preserved.
# R6-M717 RETIRED TASKS rich_3296 block line 31/31 — return-to-6; line-count preserved.
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
    """fastapi_14794""": {"repo": """fastapi/fastapi""", "base": """464c359bb03f""", "test_patch": """--- a/tests/test_response_dependency.py\n+++ b/tests/test_response_dependency.py\n@@ -0,0 +1,173 @@\n""" """+\"\"\"Test using special types (Response, Request, BackgroundTasks) as dependency annotations.\n+\n""" """+These tests verify that special FastAPI types can be used with Depends() annotations\n""" """+and that the dependency injection system properly handles them.\n+\"\"\"\n+\n+from typing import Annotated\n+\n""" """+from fastapi import BackgroundTasks, Depends, FastAPI, Request, Response\n+from fastapi.responses import JSONResponse\n""" """+from fastapi.testclient import TestClient\n+\n+\n+def test_response_with_depends_annotated():\n""" """+    \"\"\"Response type hint should work with Annotated[Response, Depends(...)].\"\"\"\n+    app = FastAPI()\n+\n""" """+    def modify_response(response: Response) -> Response:\n+        response.headers[\"X-Custom\"] = \"modified\"\n+        return response\n+\n""" """+    @app.get(\"/\")\n+    def endpoint(response: Annotated[Response, Depends(modify_response)]):\n+        return {\"status\": \"ok\"}\n+\n""" """+    client = TestClient(app)\n+    resp = client.get(\"/\")\n+\n+    assert resp.status_code == 200\n+    assert resp.json() == {\"status\": \"ok\"}\n""" """+    assert resp.headers.get(\"X-Custom\") == \"modified\"\n+\n+\n+def test_response_with_depends_default():\n""" """+    \"\"\"Response type hint should work with Response = Depends(...).\"\"\"\n+    app = FastAPI()\n+\n""" """+    def modify_response(response: Response) -> Response:\n+        response.headers[\"X-Custom\"] = \"modified\"\n+        return response\n+\n""" """+    @app.get(\"/\")\n+    def endpoint(response: Response = Depends(modify_response)):\n+        return {\"status\": \"ok\"}\n+\n+    client = TestClient(app)\n""" """+    resp = client.get(\"/\")\n+\n+    assert resp.status_code == 200\n+    assert resp.json() == {\"status\": \"ok\"}\n""" """+    assert resp.headers.get(\"X-Custom\") == \"modified\"\n+\n+\n+def test_response_without_depends():\n""" """+    \"\"\"Regular Response injection should still work.\"\"\"\n+    app = FastAPI()\n+\n+    @app.get(\"/\")\n+    def endpoint(response: Response):\n""" """+        response.headers[\"X-Direct\"] = \"set\"\n+        return {\"status\": \"ok\"}\n+\n+    client = TestClient(app)\n+    resp = client.get(\"/\")\n+\n""" """+    assert resp.status_code == 200\n+    assert resp.json() == {\"status\": \"ok\"}\n+    assert resp.headers.get(\"X-Direct\") == \"set\"\n+\n+\n""" """+def test_response_dependency_chain():\n+    \"\"\"Response dependency should work in a chain of dependencies.\"\"\"\n+    app = FastAPI()\n+\n""" """+    def first_modifier(response: Response) -> Response:\n+        response.headers[\"X-First\"] = \"1\"\n+        return response\n+\n""" """+    def second_modifier(\n+        response: Annotated[Response, Depends(first_modifier)],\n+    ) -> Response:\n""" """+        response.headers[\"X-Second\"] = \"2\"\n+        return response\n+\n+    @app.get(\"/\")\n""" """+    def endpoint(response: Annotated[Response, Depends(second_modifier)]):\n+        return {\"status\": \"ok\"}\n+\n+    client = TestClient(app)\n""" """+    resp = client.get(\"/\")\n+\n+    assert resp.status_code == 200\n+    assert resp.headers.get(\"X-First\") == \"1\"\n""" """+    assert resp.headers.get(\"X-Second\") == \"2\"\n+\n+\n+def test_response_dependency_returns_different_response_instance():\n""" """+    \"\"\"Dependency that returns a different Response instance should work.\n+\n""" """+    When a dependency returns a new Response object (e.g., JSONResponse) instead\n""" """+    of modifying the injected one, the returned response should be used and any\n+    modifications to it in the endpoint should be preserved.\n""" """+    \"\"\"\n+    app = FastAPI()\n+\n+    def default_response() -> Response:\n+        response = JSONResponse(content={\"status\": \"ok\"})\n""" """+        response.headers[\"X-Custom\"] = \"initial\"\n+        return response\n+\n+    @app.get(\"/\")\n""" """+    def endpoint(response: Annotated[Response, Depends(default_response)]):\n+        response.headers[\"X-Custom\"] = \"modified\"\n""" """+        return response\n+\n+    client = TestClient(app)\n+    resp = client.get(\"/\")\n+\n+    assert resp.status_code == 200\n""" """+    assert resp.json() == {\"status\": \"ok\"}\n+    assert resp.headers.get(\"X-Custom\") == \"modified\"\n+\n+\n+# Tests for Request type hint with Depends\n""" """+def test_request_with_depends_annotated():\n+    \"\"\"Request type hint should work in dependency chain.\"\"\"\n+    app = FastAPI()\n+\n""" """+    def extract_request_info(request: Request) -> dict:\n+        return {\n+            \"path\": request.url.path,\n""" """+            \"user_agent\": request.headers.get(\"user-agent\", \"unknown\"),\n+        }\n+\n+    @app.get(\"/\")\n+    def endpoint(\n""" """+        info: Annotated[dict, Depends(extract_request_info)],\n+    ):\n+        return info\n+\n+    client = TestClient(app)\n""" """+    resp = client.get(\"/\", headers={\"user-agent\": \"test-agent\"})\n+\n+    assert resp.status_code == 200\n""" """+    assert resp.json() == {\"path\": \"/\", \"user_agent\": \"test-agent\"}\n+\n+\n+# Tests for BackgroundTasks type hint with Depends\n""" """+def test_background_tasks_with_depends_annotated():\n+    \"\"\"BackgroundTasks type hint should work with Annotated[BackgroundTasks, Depends(...)].\"\"\"\n""" """+    app = FastAPI()\n+    task_results = []\n+\n+    def background_task(message: str):\n+        task_results.append(message)\n+\n""" """+    def add_background_task(background_tasks: BackgroundTasks) -> BackgroundTasks:\n""" """+        background_tasks.add_task(background_task, \"from dependency\")\n+        return background_tasks\n+\n+    @app.get(\"/\")\n+    def endpoint(\n""" """+        background_tasks: Annotated[BackgroundTasks, Depends(add_background_task)],\n+    ):\n""" """+        background_tasks.add_task(background_task, \"from endpoint\")\n+        return {\"status\": \"ok\"}\n+\n+    client = TestClient(app)\n""" """+    resp = client.get(\"/\")\n+\n+    assert resp.status_code == 200\n+    assert \"from dependency\" in task_results\n""" """+    assert \"from endpoint\" in task_results\n\n"""},
    """fastapi_14485""": {"repo": """fastapi/fastapi""", "base": """60699f306b67""", "test_patch": """--- a/tests/test_stringified_annotation_dependency.py\n+++ b/tests/test_stringified_annotation_dependency.py\n@@ -0,0 +1,80 @@\n+from __future__ import annotations\n+\n+from typing import TYPE_CHECKING\n+\n+import pytest\n+from fastapi import Depends, FastAPI\n+from fastapi.testclient import TestClient\n+from inline_snapshot import snapshot\n+from typing_extensions import Annotated\n+\n+if TYPE_CHECKING:  # pragma: no cover\n+    from collections.abc import AsyncGenerator\n+\n+\n+class DummyClient:\n+    async def get_people(self) -> list:\n+        return [\"John Doe\", \"Jane Doe\"]\n+\n+    async def close(self) -> None:\n+        pass\n+\n+\n+async def get_client() -> AsyncGenerator[DummyClient, None]:\n+    client = DummyClient()\n+    yield client\n+    await client.close()\n+\n+\n+Client = Annotated[DummyClient, Depends(get_client)]\n+\n+\n+@pytest.fixture(name=\"client\")\n+def client_fixture() -> TestClient:\n+    app = FastAPI()\n+\n+    @app.get(\"/\")\n+    async def get_people(client: Client) -> list:\n+        return await client.get_people()\n+\n+    client = TestClient(app)\n+    return client\n+\n+\n+def test_get(client: TestClient):\n+    response = client.get(\"/\")\n+    assert response.status_code == 200, response.text\n+    assert response.json() == [\"John Doe\", \"Jane Doe\"]\n+\n+\n+def test_openapi_schema(client: TestClient):\n+    response = client.get(\"/openapi.json\")\n+    assert response.status_code == 200, response.text\n+    assert response.json() == snapshot(\n+        {\n+            \"openapi\": \"3.1.0\",\n+            \"info\": {\"title\": \"FastAPI\", \"version\": \"0.1.0\"},\n+            \"paths\": {\n+                \"/\": {\n+                    \"get\": {\n+                        \"summary\": \"Get People\",\n+                        \"operationId\": \"get_people__get\",\n+                        \"responses\": {\n+                            \"200\": {\n+                                \"description\": \"Successful Response\",\n+                                \"content\": {\n+                                    \"application/json\": {\n+                                        \"schema\": {\n+                                            \"items\": {},\n+                                            \"type\": \"array\",\n+                                            \"title\": \"Response Get People  Get\",\n+                                        }\n+                                    }\n+                                },\n+                            }\n+                        },\n+                    }\n+                }\n+            },\n+        }\n+    )"""},
}
REWRITE_LOW_TERSE = {"model": "tinfoil/gemma4-31b", "reasoningEffort": "low"}
FILE_HINTS = {
    "fastapi_14786": "Edit ONLY fastapi/security/utils.py (get_authorization_scheme_param, add .strip()).",
    "fastapi_13537": "Edit ONLY fastapi/dependencies/utils.py (_extract_form_body / visited fields + extra-key fix). Do NOT touch fastapi/routing.py.",
    """rich_3905""": "Edit ONLY rich/progress.py (Progress start/stop symmetry).",
    "fastapi_14258": "Edit ONLY fastapi/routing.py (APIRouter.include_router self-guard, AssertionError).",
    "fastapi_15589": "Edit ONLY fastapi/dependencies/utils.py (query/cookie/header model extra params). Output a REAL diff, never empty.",
    """rich_3894""": "Edit ONLY rich/_inspect.py (_get_signature qualname fallback).",
# R6-M717 RETIRED FILE_HINTS rich_2725 — return-to-6 (same-6 ladder); line-count preserved.
# R6-M717 RETIRED FILE_HINTS rich_3296 — return-to-6 (same-6 ladder); line-count preserved.
    """rich_2725""": "Edit ONLY rich/table.py (box mid/foot ordering in _render).",
    """rich_3296""": "Edit ONLY rich/syntax.py (__rich_console__ padding style).",
    "fastapi_14794": "Edit ONLY fastapi/dependencies/utils.py (analyze_param: check Depends before Response special-casing; see tests/test_response_dependency.py).",
    "fastapi_14485": "Edit ONLY fastapi/dependencies/utils.py (_get_signature eval_str-try/fallback in get_typed_signature/get_typed_return_annotation).",
}
EDGE_HINTS = {
    "fastapi_14786": "Must return scheme, param.strip().",
    "fastapi_13537": "Track visited fields, keep extra-key fix, correct file only.",
    """rich_3905""": "Repro disabled non-interactive track first; symmetric gate.",
    "fastapi_14258": "Raise AssertionError with exact message on router.include_router(router).",
    "fastapi_15589": "Non-empty diff required; empty output = FAIL, retry.",
    """rich_3894""": "Repro lru_cache + __slots__ inspect first; type-check fallback.",
# R6-M717 RETIRED EDGE_HINTS rich_2725 — return-to-6 (same-6 ladder); line-count preserved.
# R6-M717 RETIRED EDGE_HINTS rich_3296 — return-to-6 (same-6 ladder); line-count preserved.
    """rich_2725""": "Repro box-order matrix first; mid-before-foot.",
    """rich_3296""": "Padding wrapper must use the base style, not the theme background style.",
    "fastapi_14794": "Response + Depends: call the dependency normally and use its return value; never assert on the type.",
    "fastapi_14485": "TYPE_CHECKING strings need eval_str attempt with NameError fallback; resolve from unwrapped globals; correct file only.",
}
ORACLES = {
    "fastapi_14786": "ORACLE: return scheme, param.strip().",
    "fastapi_13537": "ORACLE: track visited fields; extra keys pass through; correct file only.",
    """rich_3905""": "",
    "fastapi_14258": "ORACLE: raise AssertionError with EXACT message: Cannot include the same APIRouter instance into itself. Did you mean to include a different router? (test uses match= on this string).",
    "fastapi_15589": "ORACLE: mark BOTH the converted alias and the original field alias as processed (gold adds processed_keys for the lookup alias AND get_validation_alias(field)); non-empty diff required; empty output = FAIL.",
    """rich_3894""": "",
# R6-M717 RETIRED ORACLES rich_2725 — return-to-6 (same-6 ladder); line-count preserved.
# R6-M717 RETIRED ORACLES rich_3296 — return-to-6 (same-6 ladder); line-count preserved.
    """rich_2725""": "",
    """rich_3296""": "",
    "fastapi_14794": "ORACLE: in analyze_param, check Depends before Response special handling; correct file fastapi/dependencies/utils.py only.",
    "fastapi_14485": "ORACLE: _get_signature tries inspect.signature(call, eval_str=True), except NameError retries plain; both typed getters use it.",
}
PROMPTS["fastapi_15589"] += "\n" + FILE_HINTS["fastapi_15589"]
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
            if mi <= i + 1 or ei <= mi:
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
# R6-M717 RETIRED PYTESTS rich_2725 — return-to-6 (same-6 ladder); line-count preserved.
# R6-M717 RETIRED PYTESTS rich_3296 — return-to-6 (same-6 ladder); line-count preserved.
    """rich_2725""": "tests/test_table.py -k test_placement_table_box_elements",
    """rich_3296""": "tests/test_syntax.py -k test_background_color_override_includes_padding",
    "fastapi_14794": "tests/test_response_dependency.py -k test_response_with_depends_annotated",
    "fastapi_14485": "tests/test_stringified_annotation_dependency.py -k \"test_get or test_openapi_schema\"",
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
        sh("pip install -q fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2 inline-snapshot sqlalchemy 2>&1 | tail -1", timeout=300)
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
    trc, tout = sh("cd " + work + " && " + pyenv + " python -m pytest " + tf + " -v --tb=short -W ignore::PendingDeprecationWarning -W ignore::DeprecationWarning -p no:cacheprovider -p no:unraisableexception > pytest_out.txt 2>&1; echo PYTEST_RC=$?; tail -15 pytest_out.txt", timeout=300)
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
        for pid in t2pids:  # R6: T2 net restored (return-to-6 baseline, M717)
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

# C6: entry point moved to file end (main_c defined below)

# C6-COMPOSITE (M719): paired slots. ONE reply fixes TWO halves across two repos.
# Slot counts iff BOTH halves hit testrc=0. Shakedown vehicle: diagnose-only on fail.
COMPOSITE_GROUPS = {
    "C1": ["fastapi_14786", "rich_3905"],
    "C2": ["fastapi_13537", "rich_3894"],
    "C3": ["fastapi_14258", "rich_2725"],
    "C4": ["fastapi_15589", "rich_3296"],
    "C5": ["fastapi_14794", "rich_3894"],
    "C6": ["fastapi_14485", "rich_3296"],
}
BT = chr(96) + chr(96) + chr(96)
COMPOSITE_HEADER = CONTRACT
COMPOSITE_MID = "\nPAIRED-SLOT ADDENDUM (both halves REQUIRED -- same GOODRUN envelope, no extra budget):\n- Emit at least one FILE block per half in ONE reply (HALF A and HALF B both REQUIRED; covering one half scores the slot empty).\n- Allowed files are listed per half below; a FILE path outside the half\u0027s list voids the reply.\n- Minimal fix per half; no cross-contamination (SEARCH text from one repo never applies to the other)."
COMPOSITE_TAIL = "Repeat the CONTRACT shape per hunk; several FILE sections allowed (at least one per half). SEARCH must occur in the target file byte-for-byte exactly once."
# COMPOSITE_TAIL removed M724 (replaced by CONTRACT-verbatim header + precise TAIL above)
def build_composite_prompt(a, b):
    return (COMPOSITE_HEADER + COMPOSITE_MID + chr(10) + "Allowed HALF A files: " + str(ALLOW[a]) + chr(10) + "Allowed HALF B files: " + str(ALLOW[b]) + chr(10) + chr(10) + "HALF A (" + a + "):" + chr(10) + ISSUES[a] + chr(10) + chr(10) + "LOCALIZED CODE A (verbatim from the base commit; SEARCH blocks must be copied from here byte-for-byte):" + chr(10) + SLICES[a] + chr(10) + chr(10) + "HALF B (" + b + "):" + chr(10) + ISSUES[b] + chr(10) + chr(10) + "LOCALIZED CODE B (verbatim from the base commit; SEARCH blocks must be copied from here byte-for-byte):" + chr(10) + SLICES[b] + chr(10) + COMPOSITE_TAIL)
COMPOSITE_PROMPTS = {}
for _cid, (_ha, _hb) in COMPOSITE_GROUPS.items():
    COMPOSITE_PROMPTS[_cid] = build_composite_prompt(_ha, _hb)
def serialize_blocks(blocks):
    out = []
    for (p, s, r) in blocks:
        out.append("FILE: " + p + chr(10) + "<<<< SEARCH" + chr(10) + s + chr(10) + "======" + chr(10) + r + chr(10) + ">>>>>>")
    return chr(10).join(out) + chr(10)
async def ask_c(s, cid, prompt, ok):
    full = "Emit FILE:/SEARCH/REPLACE triples for BOTH halves in one reply." + chr(10) + chr(10) + prompt
    last = ""
    for attempt in range(3):
        q = full if attempt == 0 else "INVALID prior output (unparseable, wrong FILE, or a half missing). Resubmit COMPLETE BLOCKS FOR BOTH HALVES, correct FILEs, SEARCH verbatim." + chr(10) + chr(10) + full
        reply = await s.send(q, rewrite=REWRITE_LOW_TERSE)
        last = reply
        b = reply.strip()
        if b.startswith(BT):
            ls = b.split(chr(10))
            b = chr(10).join(ls[1:-1] if ls[-1].strip().startswith(BT) else ls[1:])
        bl = _parse_blocks(b)
        halves = set()
        if bl and all(p in ok for (p, _s, _r) in bl):
            for (p, _s, _r) in bl:
                for h in COMPOSITE_GROUPS[cid]:
                    if p in ALLOW.get(h, []):
                        halves.add(h)
            if len(halves) == 2:
                return reply.replace(BT, "")
        print("RETRY-C " + cid + " attempt=" + str(attempt + 1) + " len=" + str(len(reply)), flush=True)
    return last
def harness_c(cid, reply):
    halves = COMPOSITE_GROUPS[cid]
    ok = ALLOW.get(halves[0], []) + ALLOW.get(halves[1], [])
    body = reply.strip()
    if body.startswith(BT):
        ls = body.split(chr(10))
        body = chr(10).join(ls[1:-1] if ls[-1].strip().startswith(BT) else ls[1:])
    blocks = _parse_blocks(body)
    if not blocks:
        FAIL_TAILS[cid] = "no parseable blocks in composite reply len=" + str(len(body))
        return "empty len=" + str(len(body))
    for (path, _s, _r) in blocks:
        if path not in ok:
            FAIL_TAILS[cid] = "wrong FILE " + path
            return "wrong-file " + path
    subs = {}
    for h in halves:
        subs[h] = []
    for (path, search, repl) in blocks:
        owner = next(h for h in halves if path in ALLOW.get(h, []))
        subs[owner].append((path, search, repl))
    for h in halves:
        if not subs[h]:
            FAIL_TAILS[cid] = "half " + h + " has NO blocks"
            return "empty half=" + h
    res = {}
    for h in halves:
        sub = serialize_blocks(subs[h])
        res[h] = harness(h, sub, TASKS[h])
    trcs = {}
    for h in halves:
        import re as _re2
        _m2 = _re2.search(r"testrc=(\d+)", res[h])
        trcs[h] = _m2.group(1) if _m2 else "?"
    print("TEST-RESULT " + cid + " " + halves[0] + "=" + trcs[halves[0]] + " " + halves[1] + "=" + trcs[halves[1]], flush=True)
    bad = [h for h in halves if trcs[h] != "0"]
    if bad:
        FAIL_TAILS[cid] = "composite fail: " + ", ".join(h + "=" + trcs[h] for h in halves)
        for h in halves:
            if res[h].startswith("search-miss") or res[h].startswith("empty") or res[h].startswith("wrong-file"):
                return res[h].replace(h, cid + ":" + h, 1)
        return "testrc=1 " + cid
    return "collected " + cid + " testrc=0/0"
async def main_c():
    s = DuckAISession(model="tinfoil/gemma4-31b", timeout=240.0)
    results = {}
    replies = {}
    if True:
        for cid in COMPOSITE_GROUPS:
            halves = COMPOSITE_GROUPS[cid]
            ok = ALLOW.get(halves[0], []) + ALLOW.get(halves[1], [])
            print("=== COMPOSITE " + cid + " ===", flush=True)
            try:
                reply = await ask_c(s, cid, COMPOSITE_PROMPTS[cid], ok)
            except Exception as e:
                print("CHAT-FAIL " + cid + " " + str(e)[:300], flush=True)
                results[cid] = "chat-fail"
                continue
            print("REPLY-OK " + cid + " len=" + str(len(reply)), flush=True)
            replies[cid] = reply
            try:
                os.makedirs("/tmp/duck6_out", exist_ok=True)
                open("/tmp/duck6_out/" + cid + ".reply.txt", "w").write(reply)
            except Exception as e:
                print("REPLY-SAVE-FAIL " + cid + " " + str(e)[:120], flush=True)
    for cid in replies:
        res = harness_c(cid, replies[cid])
        results[cid] = res
        print("SCORED-COLLECTED " + cid + " " + res, flush=True)
    try:
        t2cids = []
        for cid, res in results.items():
            if res.startswith("search-miss") or res.startswith("empty") or res.startswith("wrong-file"):
                t2cids.append(cid)
            elif "testrc=1" in res:
                t2cids.append(cid)
        for cid in t2cids:
            tail = FAIL_TAILS.get(cid, "")[-1500:]
            fb = ("HARNESS FEEDBACK for " + cid + ":" + chr(10) + tail + chr(10) + "Resubmit COMPLETE BLOCKS FOR BOTH HALVES." + chr(10) + chr(10) + COMPOSITE_PROMPTS[cid])
            try:
                reply2 = await s.send(fb, rewrite=REWRITE_LOW_TERSE)
            except Exception as e:
                print("TURN2-FAIL " + cid + " " + str(e)[:200], flush=True)
                continue
            print("REPLY2-OK " + cid + " len=" + str(len(reply2)), flush=True)
            try:
                open("/tmp/duck6_out/" + cid + ".reply2.txt", "w").write(reply2)
            except Exception:
                pass
            res2 = harness_c(cid, reply2)
            results[cid] = res2 + " [turn2]"
            print("SCORED-COLLECTED-T2 " + cid + " " + results[cid], flush=True)
    finally:
        await s.close()
    print("STAGEA-RESULTS " + str(results), flush=True)
asyncio.run(main_c())
