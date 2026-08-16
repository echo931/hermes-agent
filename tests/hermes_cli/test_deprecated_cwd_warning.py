"""Tests for warn_deprecated_cwd_env_vars() migration warning."""


class TestDeprecatedCwdWarning:
    """Warn when MESSAGING_CWD or TERMINAL_CWD is set in .env."""

    def test_messaging_cwd_triggers_warning(self, monkeypatch, capsys):
        import hermes_cli.config as config_module

        monkeypatch.setattr(config_module, "load_env", lambda: {"MESSAGING_CWD": "/some/path"})
        warn_deprecated_cwd_env_vars = config_module.warn_deprecated_cwd_env_vars
        warn_deprecated_cwd_env_vars(config={})

        captured = capsys.readouterr()
        assert "MESSAGING_CWD" in captured.err
        assert "deprecated" in captured.err.lower()
        assert "config.yaml" in captured.err


    def test_both_deprecated_vars_warn(self, monkeypatch, capsys):
        import hermes_cli.config as config_module

        monkeypatch.setattr(
            config_module,
            "load_env",
            lambda: {"MESSAGING_CWD": "/msg/path", "TERMINAL_CWD": "/term/path"},
        )
        warn_deprecated_cwd_env_vars = config_module.warn_deprecated_cwd_env_vars
        warn_deprecated_cwd_env_vars(config={})

        captured = capsys.readouterr()
        assert "MESSAGING_CWD" in captured.err
        assert "TERMINAL_CWD" in captured.err

    def test_bridged_process_terminal_cwd_does_not_warn(self, monkeypatch, capsys):
        import hermes_cli.config as config_module

        monkeypatch.setenv("TERMINAL_CWD", "/bridged/by/gateway")
        monkeypatch.setattr(config_module, "load_env", lambda: {})

        config_module.warn_deprecated_cwd_env_vars(config={})

        assert capsys.readouterr().err == ""
