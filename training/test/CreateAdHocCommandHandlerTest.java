import org.apache.fineract.adhocquery.handler.CreateAdHocCommandHandler;
import org.apache.fineract.adhocquery.service.AdHocWritePlatformService;
import org.apache.fineract.infrastructure.core.api.JsonCommand;
import org.apache.fineract.infrastructure.core.data.CommandProcessingResult;
import org.junit.Before;
import org.junit.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.mockito.Mockito.*;

public class CreateAdHocCommandHandlerTest {

    @InjectMocks
    private CreateAdHocCommandHandler createAdHocCommandHandler;

    @Mock
    private AdHocWritePlatformService writePlatformService;

    @Before
    public void setup() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testProcessCommandSuccess() {
        JsonCommand command = mock(JsonCommand.class);
        when(writePlatformService.createAdHocQuery(any(JsonCommand.class))).thenReturn(new CommandProcessingResult(1L));
        CommandProcessingResult result = createAdHocCommandHandler.processCommand(command);
        verify(writePlatformService, times(1)).createAdHocQuery(any(JsonCommand.class));
    }

    @Test
    public void testProcessCommandFailure() {
        JsonCommand command = mock(JsonCommand.class);
        when(writePlatformService.createAdHocQuery(any(JsonCommand.class))).thenThrow(new RuntimeException());
        CommandProcessingResult result = createAdHocCommandHandler.processCommand(command);
        verify(writePlatformService, times(1)).createAdHocQuery(any(JsonCommand.class));
    }

    @Test
    public void testProcessCommandWithDifferentInput() {
        JsonCommand command = mock(JsonCommand.class);
        when(writePlatformService.createAdHocQuery(any(JsonCommand.class))).thenReturn(new CommandProcessingResult(2L));
        CommandProcessingResult result = createAdHocCommandHandler.processCommand(command);
        verify(writePlatformService, times(1)).createAdHocQuery(any(JsonCommand.class));
    }
}