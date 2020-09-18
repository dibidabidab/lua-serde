env["setComponents"] = [&](int entity, const sol::table &componentsTable) {

        for (const auto &[componentName, comp] : componentsTable)
        {
            if (!componentName.is<std::string>())
                throw gu_err("All keys in the components table must be a string!");

            auto nameStr = componentName.as<std::string>();

            if (!comp.is<sol::table>())
                throw gu_err("Expected a table for " + nameStr);
            luaTableToComponent(entt::entity(entity), nameStr, comp);
        }
    };
