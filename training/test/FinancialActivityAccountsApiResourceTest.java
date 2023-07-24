import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.apache.fineract.commands.service.CommandProcessingResult;
import org.apache.fineract.commands.service.CommandsSourceWritePlatformService;
import org.apache.fineract.infrastructure.core.serialization.ApiJsonSerializerService;
import org.apache.fineract.commands.domain.CommandWrapper;
import org.apache.fineract.commands.domain.CommandWrapperBuilder;

import static org.mockito.Mockito.*;

public class FinancialActivityAccountsApiResourceTest {

    @InjectMocks
    FinancialActivityAccountsApiResource financialActivityAccountsApiResource;

    @Mock
    CommandsSourceWritePlatformService commandsSourceWritePlatformService;

    @Mock
    ApiJsonSerializerService apiJsonSerializerService;

    @BeforeEach
    public void init() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testCreateGLAccount_WhenCommandProcessingResultIsSuccessful() {
        CommandWrapper commandRequest = new CommandWrapperBuilder().createOfficeToGLAccountMapping().withJson("{}").build();
        CommandProcessingResult result = mock(CommandProcessingResult.class);
        when(commandsSourceWritePlatformService.logCommandSource(commandRequest)).thenReturn(result);
        when(apiJsonSerializerService.serialize(result)).thenReturn("{}");
        financialActivityAccountsApiResource.createGLAccount("{}");
        verify(apiJsonSerializerService, times(1)).serialize(result);
    }

    @Test
    public void testCreateGLAccount_WhenCommandProcessingResultIsNull() {
        CommandWrapper commandRequest = new CommandWrapperBuilder().createOfficeToGLAccountMapping().withJson("{}").build();
        when(commandsSourceWritePlatformService.logCommandSource(commandRequest)).thenReturn(null);
        financialActivityAccountsApiResource.createGLAccount("{}");
        verify(apiJsonSerializerService, times(0)).serialize(any());
    }

    @Test
    public void testCreateGLAccount_WhenJsonRequestBodyIsNull() {
        CommandWrapper commandRequest = new CommandWrapperBuilder().createOfficeToGLAccountMapping().withJson(null).build();
        CommandProcessingResult result = mock(CommandProcessingResult.class);
        when(commandsSourceWritePlatformService.logCommandSource(commandRequest)).thenReturn(result);
        when(apiJsonSerializerService.serialize(result)).thenReturn("{}");
        financialActivityAccountsApiResource.createGLAccount(null);
        verify(apiJsonSerializerService, times(1)).serialize(result);
    }
}
